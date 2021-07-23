import fastapi

from services.openweather import get_report_async
from api_models.weather import WeatherReport

v1 = fastapi.APIRouter()

@v1.get('/weather', response_model=WeatherReport)
async def weather():
    report = await get_report_async('Portland', 'OR', 'US', 'imperial')
    return report
