import fastapi

v1 = fastapi.APIRouter()

@v1.get('/async-ping')
...