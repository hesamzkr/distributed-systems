import asyncio
from datetime import timedelta
import random
import requests
from config import config
from aiobreaker import CircuitBreaker
from httpx import AsyncClient, HTTPError, RequestError, Timeout

breaker = CircuitBreaker(fail_max=5, timeout_duration=timedelta(seconds=60))

async def make_request_with_retries(url, json, max_retries=5, backoff_factor=0.5):
    async with AsyncClient() as client:
        for retry in range(max_retries):
            try:
                response = await client.post(url, json=json, timeout=Timeout(10.0, read=20.0))
                response.raise_for_status()
                return response
            except (HTTPError, RequestError) as e:
                if retry == max_retries - 1:
                    raise
                wait_time = backoff_factor * (2 ** retry) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)


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