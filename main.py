from fastapi import FastAPI

from routers import courier_router

app = FastAPI()

app.include_router(courier_router, tags=["courier"])
