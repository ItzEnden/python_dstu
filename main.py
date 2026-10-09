from fastapi import FastAPI, Request
from fastapi.param_functions import Body

from api.v1 import tasks_router, users_router
from core.database import Base, engine


app = FastAPI()

app.include_router(tasks_router)
app.include_router(users_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"msg": "Hi"}


@app.post("/v1/debug")
async def debug(request: Request, json_data = Body(...)):
    body = await request.body()
    body = body.decode("utf-8")
    # json_data = await request.json()
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    ip = request.client.host if request.client is not None else None

    return {"ip": ip, "body": body, "query_params": query_params, "headers": headers, "json_data": json_data}
