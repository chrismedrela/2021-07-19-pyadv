from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr, validator


class WeatherReport(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class Unit(str, Enum):
    standard = 'standard'
    metric = 'metric'
    imperial = 'imperial'


class GetWeatherReportRequest(BaseModel):
    city: constr(strip_whitespace=True, to_lower=True)
    state: Optional[constr(strip_whitespace=True, to_lower=True, min_length=2, max_length=2)] = None
    country: constr(strip_whitespace=True, to_lower=True, min_length=2, max_length=2) = 'us'
    units: Unit = 'metric'

    @validator('units', pre=True)
    def lower_and_strip(cls, v):
        return v.lower().strip()
