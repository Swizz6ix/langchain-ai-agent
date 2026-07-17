from unittest.mock import Mock

from app.tools.get_weather import get_weather


def test_weather(mocker):
    mock_current = Mock()
    mock_forecast = Mock()

    mock_current.json.return_value = {
        "main": {"temp": 30, "humidity": 80},
        "weather": [{"description": "sunny"}],
        "wind": {"speed": 5},
    }

    mock_forecast.json.return_value = {
        "list": [
            {
                "dt_txt": "2026-07-18 12:00:00",
                "main": {"temp": 31},
                "weather": [{"description": "clear sky"}],
            },
            {
                "dt_txt": "2026-07-18 15:00:00",
                "main": {"temp": 32},
                "weather": [{"description": "few cloud"}],
            },
        ]
    }

    mock_current.raise_for_status.return_value = None
    mock_forecast.raise_for_status.return_value = None

    mocker.patch.dict("os.environ", {"OPEN_WEATHER_API_KEY": "mock-key"})

    mocker.patch(
        "requests.get",
        side_effect=[mock_current, mock_forecast],
    )

    result = get_weather.invoke({"location": "Lagos", "units": "celsius", "include_forecast": True})

    assert result["location"] == "Lagos"
    assert result["current"]["temperature"] == 30
    assert result["current"]["humidity"] == 80
    assert result["current"]["conditions"] == "sunny"
    assert result["current"]["wind_speed"] == 5

    assert "forecast" in result
    assert len(result["forecast"]) == 2
    assert result["forecast"][0]["temperature"] == 31
