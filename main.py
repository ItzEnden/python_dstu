from fastapi import FastAPI, Request  # noqa: I001

from api.v1.tasks import router as tasks_router
from api.v1.users import router as users_router


app = FastAPI()

app.include_router(tasks_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"msg": "Hi"}
