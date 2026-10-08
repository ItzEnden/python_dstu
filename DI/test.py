import datetime
import time
from functools import lru_cache

from fastapi import Depends, FastAPI

app = FastAPI()

def get_user():
    user = {
        "name": "Vitaliy",
        "email": "Vitalya@mail.ru",
        "age": 15
    }

    user.update({
        "pet": "dog"
    })

    yield user

    print(123)

def get_test_user():
    user = {
        "name": "testUser",
        "email": "test@test",
        "age": 999
    }

    user.update({
        "test": "Test"
    })

    yield user

    print(123)


app.dependency_overrides[get_user] = get_test_user


@lru_cache
def get_settings():
    time.sleep(5)

    return {
        "version": 1,
        "app_name": "test",
        "secret_key": "pass123"
    }

def get_uptime():
    now = datetime.datetime.now().time()
    yield now


@app.get("/")
def root(user: dict = Depends(get_user)):
    return {"user": user}


@app.get("/info")
def info(settings: dict = Depends(get_settings)):
    return {"app": settings}
