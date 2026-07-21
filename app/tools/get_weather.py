import os
from typing import Any, Literal

import requests
from langchain.tools import tool
from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    """Input for weather queries."""

    location: str = Field(description="Name of the city")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", description="Temperature unit preference"
    )
    include_forecast: bool = Field(default=False, description="Include 5-day forecast")


@tool(args_schema=WeatherInput)
def get_weather(
    location: str, units: str = "celsius", include_forecast: bool = False
) -> dict[str, Any]:
    """
    Fetches the current weather for a given location using an AI assistant
    and optional forecast.

    Args:
        location (str): The name of the location (city, country, etc.) to get the weather for.
        units (str): The unit for temperature measurement ("Celsius" or "Fahrenheit").
        include_forecast (bool): If a 5 day forecast is needed

    Returns:
        str: A string containing weather information of the given location
    """
    params: dict[str, str] = {
        "q": location,
        "units": "metric" if units == "celsius" else "imperial",
        "appid": os.environ["OPEN_WEATHER_API_KEY"],
    }

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params,
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    result: dict[str, Any] = {
        "location": location,
        "current": {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "conditions": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        },
    }

    if include_forecast:
        forecast = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params=params,
            timeout=10,
        )

        forecast.raise_for_status()

        forecast_data = forecast.json()

        result["forecast"] = [
            {
                "time": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "condition": item["weather"][0]["description"],
            }
            for item in forecast_data["list"][:5]
        ]

    return result
