from fastapi import APIRouter, HTTPException
from src.services.weather_service import fetch_weather_forecast, calculate_energy_production

router = APIRouter()


@router.get("/weather/forecast")
async def get_weather_forecast(latitude: float, longitude: float):
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude values.")
    
    try:
        weather_data = fetch_weather_forecast(latitude, longitude)
        print(weather_data)
        daily = weather_data['daily']
        forecasts = []
        num_days = len(daily['time'])
        for i in range(num_days):
            date = daily['time'][i]
            weather_code = daily['weathercode'][i]
            min_temp = daily['temperature_2m_min'][i]
            max_temp = daily['temperature_2m_max'][i]
            sun_exposure = daily['sunshine_duration'][i]  # seconds
            energy_production = calculate_energy_production(sun_exposure)

            forecasts.append({
                "date": date,
                "weather_code": weather_code,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "energy": energy_production
            })
        
        return forecasts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/summary")
async def get_weekly_summary(latitude: float, longitude: float):
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude values.")
    
    try:
        weather_data = fetch_weather_forecast(latitude, longitude)
        daily = weather_data['daily']
        num_days = len(daily['time'])
        total_sun_exposure = 0
        min_temp = float('inf')
        max_temp = float('-inf')
        weather_conditions = 0

        has_pressure = 'surface_pressure_mean' in daily
        total_pressure = 0 if has_pressure else None

        for i in range(num_days):
            if has_pressure:
                total_pressure += daily['surface_pressure_mean'][i]
            total_sun_exposure += daily['sunshine_duration'][i]
            min_temp = min(min_temp, daily['temperature_2m_min'][i])
            max_temp = max(max_temp, daily['temperature_2m_max'][i])
            if daily['precipitation_sum'][i] > 0:
                weather_conditions += 1

        average_pressure = round((total_pressure / num_days),2) if has_pressure else None
        average_sun_exposure = round(total_sun_exposure / num_days / 3600,2)
        extreme_temperatures = {"min": min_temp, "max": max_temp}
        predominant_condition = "bez opadów" if weather_conditions <= 4 else "z opadami"
        
        return {
            'average_pressure': average_pressure,
            'average_sun_exposure': average_sun_exposure,
            'extreme_temperatures': extreme_temperatures,
            'summary': predominant_condition
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

