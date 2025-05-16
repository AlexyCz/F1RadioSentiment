""" TESTS SERVICE MODULE: Testing for `service.py` 60 + """
from unittest.mock import patch

import pandas as pd
import pytest

import api.src.service as service

@patch("api.src.service._process_open_f1_request")
def test_available_races_by_year(mock_f1_request):
    sample_openf1_response = [
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

    expected_grandprix_arr = ["Singapore Grand Prix"]
    expected_meetings_df = pd.DataFrame(sample_openf1_response[1:])

    mock_f1_request.return_value = sample_openf1_response

    test_meeting_df = pd.DataFrame({"year": []})
    grandprix, test_meeting_df = service.available_races_by_year(test_meeting_df, 2023)

    pd.testing.assert_frame_equal(test_meeting_df, expected_meetings_df, check_like=True)

    assert grandprix == expected_grandprix_arr
