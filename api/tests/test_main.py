from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from api.src.main import app
from api.src.store import SessionData, get_app_session_data


tester_client = TestClient(app)

@pytest.fixture
def override_get_app_session_data():
    data = SessionData()
    app.dependency_overrides[get_app_session_data] = lambda: data
    yield data

@pytest.fixture
def mock_return_participating_drivers():
    data = (
        ["Crash", "Dr. Neo", "Nitros"],                               # available_drivers
        pd.DataFrame({"driver_name": ["Crash", "Dr. Neo", "Nitros"],  # drivers_df
                                    "session_key": ["", "", ""]}),
        pd.DataFrame({"session_name": ["Race", "Race", "Race"],       # sessions_df
                                     "session_key": ["", "", ""]}),
        19991010                                                      # current_session_key
    )
    return data

@pytest.fixture
def mock_return_driver_race_radio_data():
    data = {
        "lap_duration": 90.00,
        "lap_avg_sentiment": [{"lap": 0, "sentiment": 0}],
        "radio": [{"radio_id": 0, "sentiment": 0}],
        "driver": {"driver_name": "Crash Bandicoot"}
    }
    return data


def test_read_main():
    response = tester_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


@patch("api.src.main.available_races_by_year",
       return_value=(["AUS-GP"], pd.DataFrame({"meeting_name": ["AUS-GP"]})))
def test_get_available_races_by_year(mock_available_races_by_year,
                                     override_get_app_session_data):

    expected_call_kwargs = {
        "meetings_df": pd.DataFrame({"session_key": []}),
        "year": 2024
    }

    response = tester_client.get("/api/races/2024")
    _, kwargs = mock_available_races_by_year.call_args

    assert override_get_app_session_data.desired_year == 2024
    pd.testing.assert_frame_equal(expected_call_kwargs["meetings_df"],
                                  kwargs.get("meetings_df"))
    assert kwargs.get("year") == expected_call_kwargs["year"]
    pd.testing.assert_frame_equal(override_get_app_session_data.meetings_df,
                                  pd.DataFrame({"meeting_name": ["AUS-GP"]}))

    assert response.status_code == 200
    assert response.json() == {"data": ["AUS-GP"]}


@patch("api.src.main.participating_drivers")
def test_get_participating_drivers(mock_participating_drivers,
                                   mock_return_participating_drivers,
                                   override_get_app_session_data):
    """
    Monstrosity of a test because my endpoint isn't very CRUDster of me.
    TO DO:
        ✅ mock particpating drivers.
        ✅ set a fixture that returns the mock return data
        ✅ mock dependency injection.
        ✅ check if mocked participating_drivers() was called adequately.
        ✅ see if that data is updated in the data store.
        ✅ check response code
        ✅ check response data
    """
    mock_participating_drivers.return_value = mock_return_participating_drivers

    expected_call_kwargs = {
        "drivers_df": pd.DataFrame({"session_key": []}),
        "meetings_df": pd.DataFrame({"session_key": []}),
        "sessions_df": pd.DataFrame({"session_key": []}),
        "year": 2023,
        "current_session_key": 0,
        "meeting_name": "Mexico City Grand Prix"
    }
    response = tester_client.get("api/drivers/Mexico City Grand Prix")

    _, kwargs = mock_participating_drivers.call_args

    #  Validating get_participating drivers [mock] was called correctly.
    pd.testing.assert_frame_equal(expected_call_kwargs["drivers_df"],
                                  kwargs.get("drivers_df"))
    pd.testing.assert_frame_equal(expected_call_kwargs["meetings_df"],
                                  kwargs.get("meetings_df"))
    pd.testing.assert_frame_equal(expected_call_kwargs["sessions_df"],
                                  kwargs.get("sessions_df"))

    assert expected_call_kwargs["year"] == kwargs.get("year")
    assert expected_call_kwargs["current_session_key"] == kwargs.get("current_session_key")
    assert expected_call_kwargs["meeting_name"] == kwargs.get("meeting_name")

    #  Validating current SessionData object data store was updated correctly.
    pd.testing.assert_frame_equal(mock_return_participating_drivers[1],
                                  override_get_app_session_data.drivers_df)

    pd.testing.assert_frame_equal(mock_return_participating_drivers[2],
                                  override_get_app_session_data.sessions_df)

    assert (mock_return_participating_drivers[3] ==
            override_get_app_session_data.current_session_key)

    assert response.status_code == 200
    assert response.json() == {"data": mock_return_participating_drivers[0]}


@patch("api.src.main.driver_race_radio_data")
def test_get_driver_race_data(mock_driver_race_radio_data,
                              mock_return_driver_race_radio_data,
                              override_get_app_session_data):

    mock_driver_race_radio_data.return_value = mock_return_driver_race_radio_data

    response = tester_client.get("api/races/driver_data/Crash Bandicoot")

    _, kwargs = mock_driver_race_radio_data.call_args

    pd.testing.assert_frame_equal(override_get_app_session_data.drivers_df,
                                  kwargs.get("drivers_df"))
    pd.testing.assert_frame_equal(override_get_app_session_data.sessions_df,
                                  kwargs.get("sessions_df"))

    assert (override_get_app_session_data.current_session_key ==
            kwargs.get("current_session_key"))
    assert ("Crash Bandicoot" == kwargs.get("driver_name"))

    assert response.status_code == 200
    assert response.json() == {"data": mock_return_driver_race_radio_data}
