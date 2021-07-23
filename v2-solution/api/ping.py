import asyncio
import fastapi

v1 = fastapi.APIRouter()

@v1.get('/async-ping')
async def async_ping():
    print('start processing')
    await asyncio.sleep(3)
    print('end processing')
    return {'ping': 'pong'}