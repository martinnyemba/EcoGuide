import requests
from flask import current_app


def get_weather_and_aqi(city, state, country):
    """
    Returns weather, Air Quality Index (AQI), and 3-hour interval
    forecast data for a given location.
    """
    api_key = current_app.config['OPENWEATHERMAP_API_KEY']

    # Base URLs for different OpenWeatherMap API endpoints
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    aqi_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"  # 3-hour forecast, 5 days

    # Parameters for weather data
    params = {
        'q': f"{city},{state},{country}".rstrip(','),  # Remove trailing commas
        'appid': api_key,
        'units': 'metric'
    }

    # Fetch current weather data
    response = requests.get(weather_url, params=params)

    if response.status_code != 200:
        return {'error': f'Unable to fetch weather data: {response.text}'}

    weather_data = response.json()

    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']

    # Fetch Air Quality Index (AQI) data
    aqi_params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key
    }
    aqi_response = requests.get(aqi_url, params=aqi_params)

    if aqi_response.status_code != 200:
        return {'error': f'Unable to fetch AQI data: {aqi_response.text}'}

    aqi_data = aqi_response.json()

    # Fetch 3-hour interval forecast data (limited to 5 days)
    forecast_params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    forecast_response = requests.get(forecast_url, params=forecast_params)

    if forecast_response.status_code != 200:
        return {'error': f'Unable to fetch forecast data: {forecast_response.text}'}

    forecast_data = forecast_response.json()

    return {
        'weather': weather_data,
        'aqi': aqi_data,
        'forecast': forecast_data
    }