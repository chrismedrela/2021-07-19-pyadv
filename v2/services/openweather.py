from typing import Optional

import requests

from services_models.openweather import WeatherReport


def get_report_async(city: str, state: Optional[str], country: str, units: str) -> WeatherReport:
    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    api_key = "6e54718561e593ab6de4b10b8c1caeed"
    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'

    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()

    report = WeatherReport(**data['main'])
    
    return report
