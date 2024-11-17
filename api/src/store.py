""" DATASTORE module contains current data store structures. """
from fastapi import Depends

import pandas as pd


class SessionData:
    def __init__(self) -> None:
        self.drivers_df = pd.DataFrame(columns=["session_key"])
        self.laps_df = pd.DataFrame(columns=["session_key"])
        self.meetings_df = pd.DataFrame(columns=["year"])
        self.radios_df = pd.DataFrame(columns=["session_key"])
        self.sessions_df = pd.DataFrame(columns=["session_key"])
        self.current_session_key = 0
        self.current_meeting_key = 0
        self.desired_year = 2023


app_session_data = SessionData()


def get_app_session_data():
    return app_session_data

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
