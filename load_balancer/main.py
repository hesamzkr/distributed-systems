import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests

app = FastAPI()

services = []
lock = asyncio.Lock()
current_index = 0

@app.get("/redirect/{path:path}")
async def redirect(path: str):
    global current_index

    async with lock:
        healthy_services = [s for s in services if s["healthy"]]

    if not healthy_services:
        raise HTTPException(status_code=503, detail="No healthy services available")

    async with lock:
        service = healthy_services[current_index % len(healthy_services)]
        current_index += 1

    return RedirectResponse(f"{service['public_url']}/{path}", status_code=302)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(health_check())

async def health_check():
    global services
    while True:
        new_services = []
        for service in services:
            try:
                response = await asyncio.to_thread(requests.get, service["url"])
                new_services.append({"url": service["url"], "public_url": service["public_url"], "healthy": response.status_code == 200})
            except requests.RequestException:
                new_services.append({"url": service["url"], "public_url": service["public_url"], "healthy": False})

        async with lock:
            services = new_services
        await asyncio.sleep(5)

class Service(BaseModel):
    url: str
    public_url: str

@app.post("/services")
async def add_service(service: Service):
    global services
    async with lock:
        if service.url not in [s["url"] for s in services]:
            services.append({"url": service.url, "public_url": service.public_url, "healthy": True})

    return {"message": "Service has been added"}

@app.get("/services")
async def get_services():
    async with lock:
        return {"services": services}

@app.get("/")
async def root():
    return {"message": "Load balancer with round robin strategy"}