from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hi"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}