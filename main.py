from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # path operation decorator
def home():  # path operation function
    return {"hello": "World"}  # JSON
