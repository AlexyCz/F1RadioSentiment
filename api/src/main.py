""" MAIN FASTAPI APPLICATION """
import os

import assemblyai as aai
import logging
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .service import (
    available_races_by_year,
    driver_race_radio_data,
    participating_drivers,
)
from .store import SessionData, get_app_session_data

cors_origins = []
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
def init_session():
    """
    Loads necessary environment variables.
    """
    logger.info(f'Initializing api and configurations...')

    global cors_origins

    if os.getenv("VERCEL_ENV") is None:
        load_dotenv(".env.local")
        cors_origins.extend(["http://localhost:3000",
                             "http://127.0.0.1:8000",
                             "http://127.0.0.1:3000"]
        )
    else:
        cors_origins.extend(["https://sentimentvroom.vercel.app"])

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
        logger.info(f'GET available_races_by_year...')

        data.desired_year = input_year
        available_grandprix, data.meetings_df = available_races_by_year(meetings_df = data.meetings_df,
                                                                        year=data.desired_year)
        return {"data": available_grandprix}
    except Exception as e:
        logger.exception(f'Failure in getting available races by year:\n')
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/races/driver_data/{driver_name}")
def get_driver_race_data(driver_name: str,
                         data: SessionData = Depends(get_app_session_data)):
    """
        GETs all necessary driver race data object for application visualization.
            We aggregate desired information and set data up by way of filtering
            with prior inputs from user.
    """
    try:
        logger.info(f'GET driver_race_data...')
        driver_radio_data = driver_race_radio_data(drivers_df=data.drivers_df,
                                                   sessions_df=data.sessions_df,
                                                   current_session_key=data.current_session_key,
                                                   driver_name=driver_name)
        return {"data": driver_radio_data}
    except Exception as e:
        logger.exception(f'Failure in getting driver race data:\n')
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/drivers/{meeting_name}")
def get_participating_drivers(meeting_name: str,
                              data: SessionData = Depends(get_app_session_data)):
    """
        GETs all participating drivers for provided Grand Prix (e.g. `Mexico City Grand Prix`), and
            returns the full driver list.
    """
    try:
        logger.info(f'GET participating_drivers...')
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
        logger.exception('Failure getting participating drivers:\n')
        raise HTTPException(status_code=500, detail=str(e))
