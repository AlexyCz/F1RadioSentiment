""" SERVICE MODULE: Business Logic for All Endpoints """
from builtins import Exception

import assemblyai as aai
import pandas as pd
import requests

from api.src.constants import AAI_CONFIG, FormulaOneUrls, SENTIMENT_INT_MAP
from api.src.utils import convert_to_dt, standardize_with_microseconds


def available_races_by_year(meetings_df: pd.DataFrame,
                            year: int = 2023):
    """
    Finds race meeting information for given year; returns updated meetings_df (to
        update data storelist) and a list of grand prix.

    return: tuple -> (grandprix: List, meetings_df: DataFrame)
    """
    race_data = _process_open_f1_request(FormulaOneUrls.GET_MEETINGS, year=year)
    race_data_df = pd.DataFrame(race_data).iloc[1:]  # removes "pre-season testing" index [0] from meetings df

    if race_data_df.empty:
        raise Exception

    meetings_df = meetings_df.merge(race_data_df, how="outer")

    grandprix = meetings_df["meeting_name"].to_list()

    return grandprix, meetings_df


def participating_drivers(drivers_df: pd.DataFrame,
                          meetings_df: pd.DataFrame,
                          sessions_df: pd.DataFrame,
                          year: int,
                          current_session_key: int,
                          meeting_name: str = "Dutch Grand Prix"):
    """
    Finds all drivers participating in user desired Grand Prix. Returns list of
        driver name strings,along with data store dataframes and vars to update.

    return: tuple -> List,
                     drivers_df: DataFrame,
                     sessions_df: DataFrame,
                     current_session_key: int
    """
    current_meeting_df = meetings_df.loc[(meetings_df.meeting_name==meeting_name) &
                                          (meetings_df.year == year)]
    current_meeting_key = current_meeting_df["meeting_key"].values[0]

    race_session_data = _process_open_f1_request(FormulaOneUrls.GET_SESSIONS, meeting_key=current_meeting_key)
    sessions_df = sessions_df.merge(pd.DataFrame(race_session_data), how="outer")

    current_session_key = sessions_df.loc[(sessions_df.meeting_key == current_meeting_key), "session_key"].iloc[-1]

    session_drivers_data = _process_open_f1_request(FormulaOneUrls.GET_DRIVERS, session_key=current_session_key)
    drivers_df = drivers_df.merge(pd.DataFrame(session_drivers_data), how="outer")
    driver_list = drivers_df.loc[(drivers_df.session_key==current_session_key), "full_name"].to_list()

    return (driver_list,
            drivers_df,
            sessions_df,
            current_session_key)


def driver_race_radio_data(drivers_df: pd.DataFrame,
                           sessions_df: pd.DataFrame,
                           current_session_key: int,
                           driver_name: str = "Lewis HAMILTON"):
    """
    Processes and agreggates all transcribed radio data for user desired driver.
        We return the finalized object containing required data.

    return: Dict -> lap_duration: float,
                    lap_avg_sentiment: List(Dict),
                    radio: List(Dict),
                    driver: Dict
    """
    current_driver_df = drivers_df.loc[(drivers_df.full_name==driver_name) &
                                         (drivers_df.session_key==current_session_key)]

    driver_number = current_driver_df["driver_number"].iloc[-1]

    laps_data = _process_open_f1_request(FormulaOneUrls.GET_LAPS,
                                         session_key=current_session_key,
                                         driver_num=driver_number)

    current_laps_df = (pd.DataFrame(laps_data)
                       .pipe(_fill_initial_lap, sessions_df, current_session_key)
                       .apply(standardize_with_microseconds, axis=1, column="date_start")
                       .pipe(convert_to_dt, column="date_start"))

    radio_data = _process_open_f1_request(FormulaOneUrls.GET_RADIO,
                                          session_key=current_session_key,
                                          driver_num=driver_number)

    current_radios_df = (pd.DataFrame(radio_data)
                         .apply(standardize_with_microseconds, axis=1, column="date")
                         .pipe(convert_to_dt, column="date")
                         .pipe(_set_radio_lap_numbers, current_laps_df)
                         .pipe(_transcribe_radio_recordings)
                         .fillna(""))

    session_lap_time_mode = _get_lap_time_mode(current_laps_df)

    lap_sent_avg = _avg_sentiment_by_lap(current_radios_df)

    return {"lap_duration": session_lap_time_mode,
            "lap_avg_sentiment": lap_sent_avg.to_dict(orient="records"),
            "radio": current_radios_df.to_dict(orient="records"),
            "driver": current_driver_df.to_dict(orient="records")[-1]}


def _process_open_f1_request(request: FormulaOneUrls, **kwargs):
    """
    Sends Open F1 API request given request enum and respective url parameters.
        Returns the deserialized json response, prepared for processing.

    driver_num:  required for GET_LAPS, GET_RADIO
    meeting_key: required for GET_SESSIONS
    session_key: required for GET_DRIVERS, GET_LAPS, GET_RADIO
    year:        required for GET_MEETINGS

    return: Dict
    """
    resp = requests.Response()
    if request == FormulaOneUrls.GET_DRIVERS:
        get_drivers_url = FormulaOneUrls.GET_DRIVERS.value.format(session_key=
                                                                  kwargs.get("session_key"))
        resp = requests.get(get_drivers_url)

    elif request == FormulaOneUrls.GET_LAPS:
        get_laps_url = FormulaOneUrls.GET_LAPS.value.format(session_key=kwargs.get("session_key"),
                                                            driver_num=kwargs.get("driver_num"))
        resp = requests.get(get_laps_url)

    elif request == FormulaOneUrls.GET_MEETINGS:
        get_meeting_url = FormulaOneUrls.GET_MEETINGS.value.format(year=kwargs.get("year"))
        resp = requests.get(get_meeting_url)

    elif request == FormulaOneUrls.GET_RADIO:
        get_radio_url = FormulaOneUrls.GET_RADIO.value.format(session_key=kwargs.get("session_key"),
                                                              driver_num=kwargs.get("driver_num"))
        resp = requests.get(get_radio_url)

    else:
        get_sessions_url = FormulaOneUrls.GET_SESSIONS.value.format(meeting_key=
                                                                    kwargs.get("meeting_key"))
        resp = requests.get(get_sessions_url)

    if resp.ok:
        return resp.json()
    else:
        return {}


def _set_radio_lap_numbers(radios_df: pd.DataFrame, laps_df: pd.DataFrame):
    """
    Returns radios dataframe with new lap number column merged on non-exact timestamp
        criteria leveraging pandas Merge_asof() functionality.

    return: radios_df: DataFrame
    """
    radios_df = (pd.merge_asof(radios_df, laps_df[["lap_number", "date_start"]],
                              left_on="date",
                              right_on="date_start")
                              .rename(columns={"date_start": "lap_date_start"}))
    return radios_df


def _transcribe_radio_recordings(radios_df: pd.DataFrame):
    """
    Given radios dataframe, return new columns with respective transcribed audio text
        and sentiment values.

    return: radios_df: DataFrame
    """
    recordings = radios_df["recording_url"].to_list()

    transcriptions = []
    transcriber = aai.Transcriber()

    for rec_url in recordings:
        current_transcription = {"recording_url": rec_url}
        transcript = transcriber.transcribe(rec_url, AAI_CONFIG)

        if transcript.error:
            current_transcription["sentiment"] = ""
            current_transcription["conversation_analysis"] = []
            continue

        radio_sentiment = [{"sentiment": sent.sentiment.value}
                            for sent in transcript.sentiment_analysis]

        current_transcription["sentiment"] = (pd.DataFrame(radio_sentiment)["sentiment"]
                                            .map(SENTIMENT_INT_MAP)
                                            .mean())

        current_transcription["conversation_analysis"] = transcript.sentiment_analysis

        transcriptions.append(current_transcription)

    radios_df = radios_df.merge(pd.DataFrame(transcriptions), on="recording_url")
    return radios_df


def _get_lap_time_mode(laps_df: pd.DataFrame):
    """
    Returns first most common lap duration for driver.

    return: float
    """
    return laps_df["lap_duration"].mode().iloc[0]


def _avg_sentiment_by_lap(radios_df: pd.DataFrame):
    """
    Returns Series with average sentiment values with lap number as index.

    return: lap_sentiments: DataFrame
    """
    lap_sentiments = (radios_df[["lap_number", "sentiment"]]
                      .groupby(["lap_number"])
                      .mean()
                      .reset_index())
    return lap_sentiments


def _fill_initial_lap(laps_df: pd.DataFrame, sessions_df: pd.DataFrame, session_key: int):
    """
    Fills in initial lap start timestamp, if not present.

    return: laps_df: DataFrame
    """
    if pd.isna(laps_df["date_start"].iloc[0]):
        laps_df.loc[0, "date_start"] = sessions_df.loc[(sessions_df.session_key == session_key)]["date_start"].iloc[0]
    return laps_df
