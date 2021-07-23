import fastapi
import uvicorn

from api import ping, weather

api = fastapi.FastAPI()
api.include_router(ping.v1, prefix='/api/v1')
api.include_router(weather.v1, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run("main:api", port=8000, host='127.0.0.1', reload=True)
