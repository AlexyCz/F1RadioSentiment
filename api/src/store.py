""" DATASTORE module contains current data store structures. """
from fastapi import Depends

import pandas as pd


class SessionData:
    """
    API Data Store class containing all necessary data structures needed across
        all requests throughout a session.
    """
    def __init__(self,
                 drivers: dict = {"session_key": []},
                 laps: dict = {"session_key": []},
                 meetings: dict = {"year": []},
                 radios: dict = {"session_key": []},
                 sessions: dict = {"session_key": []},
                 session_key: int = 0,
                 meeting_key: int = 0,
                 year: int = 2023) -> None:

        self.drivers_df = pd.DataFrame(drivers)
        self.laps_df = pd.DataFrame(laps)
        self.meetings_df = pd.DataFrame(meetings)
        self.radios_df = pd.DataFrame(radios)
        self.sessions_df = pd.DataFrame(sessions)
        self.current_session_key = session_key
        self.current_meeting_key = meeting_key
        self.desired_year = year


app_session_data = SessionData()  # Instantiate app data store object


def get_app_session_data():
    """
    Retrieves SessionData data store object for endpoints.
    """
    return app_session_data

# Utility functions using dependency injection.
def get_session_key(data: SessionData = Depends(get_app_session_data)):
    return data.current_session_key

def get_desired_year(data: SessionData = Depends(get_app_session_data)):
    return data.desired_year

def get_drivers_df(data: SessionData = Depends(get_app_session_data)):
    return data.drivers_df

def get_meetings_df(data: SessionData = Depends(get_app_session_data)):
    return data.meetings_df

def get_sessions_df(data: SessionData = Depends(get_app_session_data)):
    return data.sessions_df
