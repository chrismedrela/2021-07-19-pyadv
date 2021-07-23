import fastapi

from services.openweather import get_report_async
from api_models.weather import WeatherReport, Location

v1 = fastapi.APIRouter()
v2 = fastapi.APIRouter()

@v1.get('/weather', response_model=WeatherReport)
async def weather():
    report = await get_report_async('Portland', 'OR', 'US', 'imperial')
    return report

@v2.get('/weather/{city}', response_model=WeatherReport)
async def weather(loc: Location = fastapi.Depends(), units: str = 'metric'):
    report = await get_report_async(loc.city, loc.state, loc.country, units)
    return report    
