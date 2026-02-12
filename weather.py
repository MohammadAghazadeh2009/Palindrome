from fastapi import FastAPI, Query, HTTPException
import httpx

app = FastAPI(title="Weather API", description="Get weather info from different providers")


OPENWEATHER_API_KEY = "a4ee6d361ef340c7bc0bfaae38dfc880"  



async def get_openweather_data(lat: float, lon: float):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from OpenWeather")

    data = response.json()
    return {
        "provider": "openweather",
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }



async def get_openmeteo_data(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Open-Meteo")

    data = response.json()
    current = data.get("current_weather", {})
    return {
        "provider": "openmeteo",
        "temperature": current.get("temperature"),
        "wind_speed": current.get("windspeed"),
        "weathercode": current.get("weathercode")
    }



@app.get("/weather")
async def get_weather(
    lat: float = Query(..., gt=-90, lt=90, description="Latitude between -90 and 90"),
    lon: float = Query(..., gt=-180, lt=180, description="Longitude between -180 and 180"),
    provider: str = Query(..., description="Weather data provider: openweather | openmeteo")
):
    provider = provider.lower()
    if provider not in ["openweather", "openmeteo"]:
        raise HTTPException(status_code=400, detail="Invalid provider. Use 'openweather' or 'openmeteo'")

    if provider == "openweather":
        return await get_openweather_data(lat, lon)
    else:
        return await get_openmeteo_data(lat, lon)
