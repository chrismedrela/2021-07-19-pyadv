from typing import Optional

import aiohttp

from infrastructure.weather_cache import weather_cache
from services_models.openweather import WeatherReport
from settings import get_settings


async def get_report_async(city: str, state: Optional[str], country: str, units: str) -> WeatherReport:
    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    api_key = get_settings().api_key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        resp = await client.get(url)
        # resp.raise_for_status()
        data = await resp.json()

    report = WeatherReport(**data['main'])
    
    return report
