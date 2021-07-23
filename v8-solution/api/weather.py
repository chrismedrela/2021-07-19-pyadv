import fastapi
import pydantic
from starlette.requests import SERVER_PUSH_HEADERS_TO_COPY

from api_models.weather import WeatherReport, Location
from services.openweather import get_report_async
from services_models.openweather import GetWeatherReportRequest
from services_models.exceptions import ServiceUnavailable

v1 = fastapi.APIRouter()
v2 = fastapi.APIRouter()

@v1.get('/weather', response_model=WeatherReport)
async def weather():
    report = await get_report_async('Portland', 'OR', 'US', 'imperial')
    return report

@v2.get('/weather/{city}', response_model=WeatherReport)
async def weather(loc: Location = fastapi.Depends(), units: str = 'metric'):
    try:
        req = GetWeatherReportRequest(city=loc.city, state=loc.state, country=loc.country, units=units)
        report = await get_report_async(req)
        return report    
    except pydantic.ValidationError as ve:
        return fastapi.responses.JSONResponse(content={'errors': ve.errors()}, status_code=400)
    except ServiceUnavailable as e:
        print("Warning: ", str(e))
        return fastapi.Response(content="Service is temporarily unavailable", status_code=503)
    except Exception as x:
        print("Error:", str(x))
        return fastapi.Response(content='Server error', status_code=500)

# @v2.get('/weather/{city}', response_model=WeatherReport)
# async def weather(loc: Location = fastapi.Depends(), units: str = 'metric'):
#     try:
#         try:
#             req = GetWeatherReportRequest(city=loc.city, state=loc.state, country=loc.country, units=units)
#         except pydantic.ValidationError as ve:
#             return fastapi.responses.JSONResponse(content={'errors': ve.errors()}, status_code=400)
#         else:
#             try:
#                 return await get_report_async(req)
#             except ServiceUnavailable as e:
#                 print("Warning: ", str(e))
#                 return fastapi.Response(content="Service is temporarily unavailable", status_code=503)        
#     except Exception as x:
#         print("Error:", str(x))
#         return fastapi.Response(content='Server error', status_code=500)