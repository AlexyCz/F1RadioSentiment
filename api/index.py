from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import AnyUrl, BaseModel, EmailStr, Field

import assemblyai as aai
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import requests

aai.settings.api_key = "API_KEY"

app = FastAPI()

transcriber = aai.Transcriber()
config = aai.TranscriptionConfig(
    sentiment_analysis=True,
    speaker_labels=True
)

now = datetime.now(timezone.utc)


# class RaceModel(BaseModel):
#     meeting_key: int | None = None
#     meeting_name: str | None = None
#     session_name: str | None = None
#     session_key: int | None = None
#     year: int | None = None

# class DriverLapModel(BaseModel):
#     driver_number: int | None = None
#     lap_times: list | None = None
#     total_laps: int | None = None

# class RadioModel(BaseModel):
#     lap_numbers: list[int] | None = None
#     timestamps: list | None = None
#     urls: list[AnyUrl] | None = None

curr_race = {
    "meeting_key": None,
    "meeting_name": None,
    "session_name": "Race",
    "session_key": None,
    "year": None
}

driver_laps = {
    "driver_number": None,
    "lap_times": None,
    "total_laps": None
}

radio_messages = {
    "lap_numbers": None,
    "timestamps": None,
    "urls": None
}

meetings = {}
session = {}
drivers = {}
laps = {}
radio = {}


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


# @app.put("/api/race/")
# def update_race(race: RaceModel):
#     update_race_encoded = jsonable_encoder(race)
#     curr_race = update_race_encoded
#     return update_race_encoded

# EXPERIMENT: change below to 'api/races/' with query params, then changing driver data endpoint to 'api/races/driver_name'
@app.get("/api/races/")
def get_available_races_by_year(year: int = 2023):
    '''Given year as input, return all Grand Prix for said Formula 1 calendar year.
       OpenF1 Endpoint: "https://api.openf1.org/v1/meetings"
    '''
    meeting_url = "https://api.openf1.org/v1/meetings?year={yr}".format(yr=year)
    resp = requests.get(meeting_url)
    meetings["df"] = pd.DataFrame(resp.json()).iloc[1:]  # removes 'pre-season testing' from meetings

    available_grandprix = meetings["df"]["meeting_name"].to_list()

    return available_grandprix


@app.get("/api/races/{driver_name}")
def get_driver_race_data(driver_name: str):
    '''
        GETs all necessary blob of info for application visualization.
            We prune and set info up by way of filtering for input driver.
    '''
    # LAPS https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8
    # RADIO https://api.openf1.org/v1/team_radio?session_key=9158&driver_number=11

    drivers["df"] = drivers["df"].loc[drivers["df"].full_name==driver_name]

    session_key = drivers["df"]["session_key"].iloc[-1]
    driver_number = drivers["df"]["driver_number"].iloc[-1]
    # print(session_key, driver_number)

    laps_url = "https://api.openf1.org/v1/laps?session_key={s_key}&driver_number={d_num}".format(s_key=session_key, 
                                                                                                 d_num=driver_number)
    resp = requests.get(laps_url)
    laps["df"] = pd.DataFrame(resp.json())

    radio_url = "https://api.openf1.org/v1/team_radio?session_key={s_key}&driver_number={d_num}".format(s_key=session_key,
                                                                                                        d_num=driver_number)
    resp = requests.get(radio_url)
    radio["df"] = pd.DataFrame(resp.json())

    if radio["df"].empty:
        return []

    recordings = radio["df"]["recording_url"].to_list()
    transcriptions = []

    for rec_url in recordings:
        transcriptions.append({"recording_url": rec_url})
        transcript = transcriber.transcribe(rec_url, config)
        
        if transcript.error:
            transcriptions[-1]["sentiments"] = ""
            transcriptions[-1]["text"] = ""
            continue
        
        radio_sentiment = [{"sentiment": sent.sentiment.value}
                            for sent in transcript.sentiment_analysis]

        transcriptions[-1]["sentiment"] = (pd.DataFrame(radio_sentiment)["sentiment"].map({"NEGATIVE": -1,
                                                                                            "NEUTRAL": 0,
                                                                                            "POSITIVE": 1})
                                                                                            .mean())
        transcriptions[-1]["text"] = transcript.text

    radio["df"] = radio["df"].merge(pd.DataFrame(transcriptions), on="recording_url")

    # total_laps = laps["df"]["lap_number"].iloc[-1]
    lap_duration_mode = laps["df"]["lap_duration"].mode().iloc[0]
    # start calculating from session.start_time and aggregating lap_duration_mode to reach radio.date of each

    start_time = pd.to_datetime(session["df"]["date_start"].iloc[0]) + pd.to_timedelta(lap_duration_mode, unit='s')
    radio["df"]["date"] = pd.to_datetime(radio["df"]["date"])
    radio["df"]["race_start"] = start_time
    radio["df"]["delta"] = (radio["df"]["date"] - radio["df"]["race_start"]).dt.total_seconds()
    radio["df"]["lap_number"] = (np.floor(radio["df"]["delta"] / lap_duration_mode)).fillna(1).astype('int')

    lap_sent_avg = radio['df'][['lap_number', 'sentiment']].groupby(['lap_number']).mean()

    return {'lap_duration': lap_duration_mode,
            'lap_sentiment': lap_sent_avg.to_dict(orient='dict')['sentiment'],
            'radio': radio['df'].to_dict(orient='records'),
            'driver': drivers['df'].to_dict(orient='records')[-1]}


@app.get("/api/drivers/{meeting_name}")
def get_participating_drivers(meeting_name: str = "Dutch Grand Prix"):
    '''
        Gets all participating drivers for provided session_key [Race ID], and returns the list.\n
        OpenF1 Endpoints: "https://api.openf1.org/v1/drivers"
    '''
    meetings["df"] = meetings["df"].loc[meetings["df"].meeting_name==meeting_name]
    meeting_key = meetings["df"]["meeting_key"].values[0]  # updating meetings dict

    sessions_url = "https://api.openf1.org/v1/sessions?session_name=Race&meeting_key={m_key}".format(m_key=meeting_key)
    resp = requests.get(sessions_url)
    session["df"] = pd.DataFrame(resp.json())
    session_key = session["df"]["session_key"].iloc[-1]

    drivers_url = "https://api.openf1.org/v1/drivers?session_key={s_key}".format(s_key=session_key)
    resp = requests.get(drivers_url)
    drivers["df"] = pd.DataFrame(resp.json())

    return drivers["df"]["full_name"].to_list()
