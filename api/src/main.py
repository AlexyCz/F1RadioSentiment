from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse, HTMLResponse, Response
from pydantic import AnyUrl, BaseModel, EmailStr, Field

import assemblyai as aai
from datetime import datetime, timezone
import json
import numpy as np
import os
import pandas as pd
import requests

from api.src.store import SessionData, get_app_session_data
from api.src.service import available_races_by_year, participating_drivers, driver_race_radio_data

app = FastAPI()


@app.on_event("startup")
def init_session_data_store():
    """
        Creates the SessionData object for current app startup instance.
    """
    # get_app_session_data()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.get("/api/races/{input_year}")
def get_available_races_by_year(input_year: int,
                                data: SessionData = Depends(get_app_session_data)):
    """
    Given year as input, return all Grand Prix for said Formula 1 calendar year.
    """
    try: 
        data.desired_year = input_year
        available_grandprix, data.meetings_df = available_races_by_year(data.meetings_df, data.desired_year)
        return {"status_code": 200,
                "data": available_grandprix}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/races/driver_data/{driver_name}")
def get_driver_race_data(driver_name: str,
                         data: SessionData = Depends(get_app_session_data)):
    """
        GETs all necessary blob of info for application visualization.
            We prune and set info up by way of filtering for input driver.
    """
    try: 
        driver_radio_data = driver_race_radio_data(data.drivers_df,
                                                   data.sessions_df,
                                                   data.current_session_key,
                                                   driver_name)
        return {"status_code": 200,
                "data": driver_radio_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/drivers/{meeting_name}")
def get_participating_drivers(meeting_name: str,
                              data: SessionData = Depends(get_app_session_data)):
    """
        Gets all participating drivers for provided session_key [Race ID], and returns the list.
    """
    try:
        (available_drivers,
         data.drivers_df,
         data.sessions_df,
         data.current_session_key) = participating_drivers(data.drivers_df,
                                                           data.meetings_df,
                                                           data.sessions_df,
                                                           data.desired_year,
                                                           data.current_session_key,
                                                           meeting_name)

        return {"status_code": 200,
                "data": available_drivers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
