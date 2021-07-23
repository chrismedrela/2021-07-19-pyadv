from typing import Optional

import aiohttp

from infrastructure.weather_cache import weather_cache
from services_models.openweather import WeatherReport, GetWeatherReportRequest
from settings import get_settings


async def get_report_async(req: GetWeatherReportRequest) -> WeatherReport:
    try:
        return weather_cache.get(req)
    except KeyError:
        if req.state:
            q = f'{req.city},{req.state},{req.country}'
        else:
            q = f'{req.city},{req.country}'

        api_key = get_settings().api_key
        url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={req.units}'

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
            resp = await client.get(url)
            data = await resp.json()

        report = WeatherReport(**data['main'])
        
        weather_cache.set(req, report)

        return report
