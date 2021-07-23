from typing import Optional

from pydantic import BaseModel


class WeatherReport(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = 'US'
