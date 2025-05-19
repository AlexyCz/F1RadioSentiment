""" TESTS SERVICE MODULE: Testing for `service.py` 60 + 30 + """
from unittest.mock import patch

import pandas as pd
from pluggy import Result
import pytest

import api.src.service as service
from api.src.store import SessionData
from api.src.constants import FormulaOneUrls


@pytest.fixture
def mock_data_store_obj():
    data_store = SessionData()
    return data_store


def mock_process_open_f1_response_data(endpoint, **kwargs):
    if endpoint == FormulaOneUrls.GET_DRIVERS:
        sample_openf1_drivers_response  = [
            {
                "broadcast_name": "M VERSTAPPEN",
                "country_code": "NED",
                "driver_number": 1,
                "first_name": "Max",
                "full_name": "Max VERSTAPPEN",
                "headshot_url": "https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
                "last_name": "Verstappen",
                "meeting_key": 1216,
                "name_acronym": "VER",
                "session_key": 9140,
                "team_colour": "3671C6",
                "team_name": "Red Bull Racing"
            }
        ]
        return sample_openf1_drivers_response

    elif endpoint == FormulaOneUrls.GET_LAPS:
        sample_openf1_laps_response  = [
            {

            }
        ]
    elif endpoint == FormulaOneUrls.GET_MEETINGS:
        sample_openf1_meetings_response = [
        {
            "circuit_key": 61,
            "circuit_short_name": "Pre-Season-Singapore",
            "meeting_name": "Singapore Testing",
            "meeting_key": 1218,
            "meeting_official_name": "FORMULA 1 PRESEASON SINGAPORE AIRLINES SINGAPORE TESTING 2023",
            "year": 2023
        },
        {
            "circuit_key": 61,
            "circuit_short_name": "Singapore",
            "meeting_name": "Singapore Grand Prix",
            "meeting_key": 1219,
            "meeting_official_name": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2023",
            "year": 2023
        }
        ]
        return sample_openf1_meetings_response

    elif endpoint == FormulaOneUrls.GET_RADIO:
        sample_openf1_radio_response  = [
            {

            }
        ]
        return sample_openf1_radio_response
    else:
        sample_openf1_sessions_response = [
            {
                "circuit_key": 61,
                "circuit_short_name": "Spa-Francorchamps",
                "country_code": "BEL",
                "country_key": 16,
                "country_name": "Belgium",
                "date_end": "2023-07-29T15:35:00+00:00",
                "date_start": "2023-07-29T15:05:00+00:00",
                "gmt_offset": "02:00:00",
                "location": "Spa-Francorchamps",
                "meeting_key": 1216,
                "session_key": 9140,
                "session_name": "Sprint",
                "session_type": "Race",
                "year": 2023
            }
        ]
        return sample_openf1_sessions_response


@patch("api.src.service._process_open_f1_request")
def test_available_races_by_year(mock_process_open_f1_request, mock_data_store_obj):
    expected_meeting_data = [
        {
            "circuit_key": 61,
            "circuit_short_name": "Singapore",
            "meeting_name": "Singapore Grand Prix",
            "meeting_key": 1219,
            "meeting_official_name": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2023",
            "year": 2023
        }
    ]
    expected_grandprix_arr = ["Singapore Grand Prix"]
    expected_meetings_df = pd.DataFrame(expected_meeting_data)

    mock_process_open_f1_request.side_effect = mock_process_open_f1_response_data

    result_grandprix, result_meeting_df = service.available_races_by_year(mock_data_store_obj.meetings_df, 2023)

    pd.testing.assert_frame_equal(result_meeting_df, expected_meetings_df, check_like=True)

    assert result_grandprix == expected_grandprix_arr


@patch("api.src.service._process_open_f1_request")
def test_participating_drivers(mock_process_open_f1_request, mock_data_store_obj):

    test_meeting_data = [
        {
            "circuit_key": 61,
            "circuit_short_name": "Spa-Francorchamps",
            "meeting_name": "Spa Grand Prix",
            "meeting_key": 1216,
            "meeting_official_name": "FORMULA 1 SPA GRAND PRIX 2023",
            "year": 2023
        }
    ]

    expected_current_session_key = 9140

    mock_process_open_f1_request.side_effect = mock_process_open_f1_response_data
    mock_data_store_obj.meetings_df = pd.DataFrame(test_meeting_data)

    (res_driver_list,
    res_drivers_df,
    res_sessions_df,
    res_current_session_key) = service.participating_drivers(
                                    mock_data_store_obj.drivers_df,
                                    mock_data_store_obj.meetings_df,
                                    mock_data_store_obj.sessions_df,
                                    mock_data_store_obj.desired_year,
                                    mock_data_store_obj.current_session_key,
                                    "Spa Grand Prix"
    )

    pd.testing.assert_frame_equal(res_drivers_df,
                                    pd.DataFrame(mock_process_open_f1_request(FormulaOneUrls.GET_DRIVERS)),
                                    check_like=True)
    pd.testing.assert_frame_equal(res_sessions_df,
                                    pd.DataFrame(mock_process_open_f1_request(FormulaOneUrls.GET_SESSIONS)),
                                    check_like=True)

    assert res_driver_list == ["Max VERSTAPPEN"]
    assert res_current_session_key == expected_current_session_key
