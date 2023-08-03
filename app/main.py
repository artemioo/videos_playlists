from fastapi import FastAPI

main_app = FastAPI()


@main_app.get("/")
async def homepage():
    return {"hello": "world"}
