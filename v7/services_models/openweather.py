from typing import Optional

from pydantic import BaseModel, constr


class WeatherReport(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class GetWeatherReportRequest(BaseModel):
    city: constr()
    state: Optional[str] = None
    country: str = 'US'
    units: Unit
