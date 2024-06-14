import asyncio
import time
import requests
from config import config

async def register_service():
    load_balancer = "http://load-balancer/services"

    service_url = config.SERVICE_URL
    public_url = config.PUBLIC_URL

    while True:
        try:
            response = await asyncio.to_thread(requests.post, load_balancer, json={"url": service_url, "public_url": public_url})
            if response.status_code == 200:
                print(response)
                print("Service registered successfully")
                break
            print(response)
        except requests.RequestException as e:
            print(f"Registration failure: {e}")
        await asyncio.sleep(5)