import requests
import os
from google.adk.tools import FunctionTool

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# The function name 'get_weather' MUST match what the agent calls.
def get_weather(location: str) -> str:
    """
    Gets the current weather for a specific location from OpenWeatherMap.
    
    Args:
        location: The city name (e.g., "San Francisco", "Tokyo", "Mumbai").
        
    Returns:
        A string describing the weather or an error message.
    """
    if not OPENWEATHER_KEY:
        return "Error: OPENWEATHER_KEY is not configured."

    params = {
        "q": location,
        "appid": OPENWEATHER_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("weather") and data.get("main"):
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            city = data["name"]
            
            return f"The current weather in {city} is {description} at {temp}°C (feels like {feels_like}°C)."
        else:
            return f"Error: Could not parse weather data for {location}."
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: City '{location}' not found."
        return f"Error: HTTP error retrieving weather: {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"

# We wrap the function *with the same name*
# The FunctionTool automatically reads the docstring for its description.
get_weather = FunctionTool(
    func=get_weather
)