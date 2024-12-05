from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from api.src.service import (
    _avg_sentiment_by_lap,
    _fill_initial_lap,
    _get_lap_time_mode,
    _process_open_f1_request,
    _set_radio_lap_numbers,
    _transcribe_radio_recordings,
    available_races_by_year,
    driver_race_radio_data,
    participating_drivers,
)

def test_avg_sentiment_by_lap():
    input_data = {
        "lap_number": [1, 2, 2],
        "sentiment": [0.555, -0.555, -1]
    }

    expected_data = {
        "lap_number": [1, 2],
        "sentiment": [0.555, -0.7775]
    }

    result_df = _avg_sentiment_by_lap(pd.DataFrame(input_data))  # radios_df

    pd.testing.assert_frame_equal(
        pd.DataFrame(expected_data),
        result_df
    )


def test_fill_initial_lap():
    input_data = {
        "laps_df": pd.DataFrame(
            {
                "lap_number": [1, 2, 3],
                "date_start": [
                    pd.NA,
                    "2023-09-16T13:59:07.606000+00:00",
                    "2023-09-16T14:00:07.606000+00:00"
                ]
            }
        ),
        "sessions_df": pd.DataFrame(
            {
                "session_key": [9140],
                "date_start": ["2023-09-16T13:30:00"]
            }
        ),
        "session_key": 9140
    }

    expected_data = {
        "lap_number": [1, 2, 3],
        "date_start": [
            "2023-09-16T13:30:00",
            "2023-09-16T13:59:07.606000+00:00",
            "2023-09-16T14:00:07.606000+00:00"
        ]
    }

    result_df = _fill_initial_lap(**input_data)  # laps_df, sessions_df, session_key

    pd.testing.assert_frame_equal(
        pd.DataFrame(expected_data),
        result_df
    )


def test_get_lap_time_mode():
    input_data = {
        "lap_number": [1, 2, 3, 4, 5],
        "lap_duration": [91.7, 91.7, 91.8, 91.8, 91.8]
    }

    expected_data = 91.8

    result = _get_lap_time_mode(pd.DataFrame(input_data))  # laps_df

    assert expected_data == result
