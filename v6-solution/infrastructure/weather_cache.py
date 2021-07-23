import datetime
import functools
import inspect
from typing import Callable, Tuple

from services_models.openweather import GetWeatherReportRequest, WeatherReport


class WeatherCache:
    def __init__(self, lifetime_in_hours=1.0):
        self.lifetime_in_hours = lifetime_in_hours
        self._cache = {}

    def get(self, req: GetWeatherReportRequest) -> WeatherReport:
        key = self.create_key(req)
        try:
            data = self._cache[key]
        except KeyError:
            raise KeyError
        else:
            last = data['time']
            dt = datetime.datetime.now() - last
            if dt / datetime.timedelta(minutes=60) < self.lifetime_in_hours:
                return data['value']
            else:
                del self._cache[key]
                raise KeyError

    def set(self, req: GetWeatherReportRequest, value: WeatherReport) -> None:
        key = self.create_key(req)
        data = {
            'time': datetime.datetime.now(),
            'value': value
        }
        self._cache[key] = data
        self._clean_out_of_date()

    def create_key(self, req: GetWeatherReportRequest) -> Tuple:
        return req.city, req.state, req.country, req.units 

    def _clean_out_of_date(self) -> None:
        for key, data in list(self._cache.items()):
            dt = datetime.datetime.now() - data['time']
            if dt / datetime.timedelta(minutes=60) > self.lifetime_in_hours:
                del self._cache[key]  

    def __call__(self, f: Callable[[GetWeatherReportRequest], WeatherReport]) \
            -> Callable[[GetWeatherReportRequest], WeatherReport]: 
        if inspect.iscoroutinefunction(f):
            @functools.wraps(f)
            async def wrapper(req: GetWeatherReportRequest) -> WeatherReport:
                try:
                    return self.get(req)
                except KeyError:
                    report = await f(req)
                    self.set(req, report)
                    return report
        else:
            @functools.wraps(f)
            def wrapper(req: GetWeatherReportRequest) -> WeatherReport:
                try:
                    return self.get(req)
                except KeyError:
                    report = f(req)
                    self.set(req, report)
                    return report
        return wrapper

weather_cache = WeatherCache()
