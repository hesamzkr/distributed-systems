import asyncio
from controllers.courier_controller import process_outbox
from utils import register_service
from fastapi import FastAPI

from routers import courier_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(register_service())
    loop.create_task(process_outbox())


app.include_router(courier_router, tags=["courier"])


@app.get("/")
def read_root():
    return {"message": "Transaction service for couriers"}
