from fastapi import FastAPI

from routers import wallet_router


app = FastAPI()

app.include_router(wallet_router, tags=["wallet"])
