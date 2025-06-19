from fastapi import HTTPException
import requests

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather_forecast(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,sunshine_duration,precipitation_sum,weathercode,surface_pressure_mean",
        "timezone": "auto"
    }
    
    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")
    
    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from weather API")
    
    return data

def calculate_energy_production(sunshine_duration: float):
    installation_power = 2.5  # kW
    efficiency = 0.2
    exposure_time_hours = sunshine_duration / 3600  
    generated_energy = installation_power * exposure_time_hours * efficiency
    return round(generated_energy, 2) 

