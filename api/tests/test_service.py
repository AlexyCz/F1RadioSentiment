from unittest.mock import patch

import pandas as pd
import pytest
# import requests
from fastapi.testclient import TestClient

from api.src.constants import FormulaOneUrls
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


@pytest.mark.parametrize("req, kwargs, expected", [
    (FormulaOneUrls.GET_DRIVERS, {"session_key": 99}, ("https://api.openf1.org/v1/drivers?session_key=99",)),
    (FormulaOneUrls.GET_LAPS, {"session_key": 99, "driver_num": 44}, ("https://api.openf1.org/v1/laps?session_key=99&driver_number=44",)),
    (FormulaOneUrls.GET_MEETINGS, {"year": 2023}, ("https://api.openf1.org/v1/meetings?year=2023",)),
    (FormulaOneUrls.GET_RADIO, {"session_key": 99, "driver_num": 44}, ("https://api.openf1.org/v1/team_radio?session_key=99&driver_number=44",)),
    (FormulaOneUrls.GET_SESSIONS, {"meeting_key": 11}, ("https://api.openf1.org/v1/sessions?session_name=Race&meeting_key=11",)),
])
@patch("api.src.service.requests.get")
def test_process_open_f1_request(mock_get_request, req, kwargs, expected):
    _process_open_f1_request(req, **kwargs)
    assert mock_get_request.call_args.args == expected
