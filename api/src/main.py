""" MAIN FASTAPI APPLICATION """
import os

import assemblyai as aai
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException

from api.src.service import (
    available_races_by_year,
    driver_race_radio_data,
    participating_drivers,
)
from api.src.store import SessionData, get_app_session_data

app = FastAPI()


@app.on_event("startup")
def init_session():
    """
    Loads necessary environment variables.
    """
    # get_app_session_data()
    if os.getenv("VERCEL_ENV") is None:
        load_dotenv(".env.local")

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
        available_grandprix, data.meetings_df = available_races_by_year(meetings_df = data.meetings_df,
                                                                        year=data.desired_year)
        return {"data": available_grandprix}
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
        driver_radio_data = driver_race_radio_data(drivers_df=data.drivers_df,
                                                   sessions_df=data.sessions_df,
                                                   current_session_key=data.current_session_key,
                                                   driver_name=driver_name)
        return {"data": driver_radio_data}
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
         data.current_session_key) = participating_drivers(drivers_df=data.drivers_df,
                                                           meetings_df=data.meetings_df,
                                                           sessions_df=data.sessions_df,
                                                           year=data.desired_year,
                                                           current_session_key=data.current_session_key,
                                                           meeting_name=meeting_name)

        return {"data": available_drivers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
