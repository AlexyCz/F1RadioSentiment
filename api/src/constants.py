""" Constants module containing recurring immutable project variables. """
from enum import Enum

class FormulaOneUrls(Enum):
    ''' OPEN-F1 ENDPOINTS '''
    GET_DRIVERS = "https://api.openf1.org/v1/drivers?session_key={session_key}"

    GET_LAPS = "https://api.openf1.org/v1/laps?session_key={session_key}&driver_number={driver_num}"

    GET_MEETINGS = "https://api.openf1.org/v1/meetings?year={year}"

    GET_RADIO = "https://api.openf1.org/v1/team_radio?session_key={session_key}&driver_number={driver_num}"

    GET_SESSIONS = "https://api.openf1.org/v1/sessions?session_name=Race&meeting_key={meeting_key}"
