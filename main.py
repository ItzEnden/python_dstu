from fastapi import FastAPI, Request
from fastapi.param_functions import Body

from api.v1.tasks import router as tasks_router
from api.v1.users import router as users_router

app = FastAPI()

app.include_router(tasks_router)
app.include_router(users_router)


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
    ip = request.client.host

    return {"ip": ip, "body": body, "query_params": query_params, "headers": headers, "json_data": json_data}