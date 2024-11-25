""" CONSTANTS MODULE: Contains recurring immutable project variables. """
from enum import Enum

import assemblyai as aai


class FormulaOneUrls(Enum):
    """ OPEN-F1 ENDPOINTS """
    GET_DRIVERS = "https://api.openf1.org/v1/drivers?session_key={session_key}"

    GET_LAPS = "https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_num}"

    GET_MEETINGS = "https://api.openf1.org/v1/meetings?year={year}"

    GET_RADIO = "https://api.openf1.org/v1/team_radio?session_key={session_key}&driver_number={driver_num}"

    GET_SESSIONS = "https://api.openf1.org/v1/sessions?session_name=Race&meeting_key={meeting_key}"



""" Assembly AI Transcriber Constants """
AAI_CONFIG = aai.TranscriptionConfig(sentiment_analysis=True,
                                     speaker_labels=True)


""" Sentiment Constants """
SENTIMENT_INT_MAP = {"NEGATIVE": -1,
                     "NEUTRAL": 0,
                     "POSITIVE": 1}
