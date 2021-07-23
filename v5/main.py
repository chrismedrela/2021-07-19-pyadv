import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import ping, weather

v1 = fastapi.APIRouter()
v1.include_router(ping.v1)
v1.include_router(weather.v1)

v2 = fastapi.APIRouter()
v2.include_router(ping.v2)
v2.include_router(weather.v2)

api = fastapi.FastAPI()
api.include_router(v1, prefix='/api/v1')
api.include_router(v2, prefix='/api/v2')
api.mount('/static', StaticFiles(directory='static'), name='static')

if __name__ == "__main__":
    uvicorn.run("main:api", port=8000, host='127.0.0.1', reload=True)
