import time
import asyncio
import httpx


N = 2


async def request(client):
    return await client.get("http://127.0.0.1:8000/asynchronous")


async def request_postgre(client):
    return await client.get("http://127.0.0.1:8000/postgre")


async def main():
    start = time.time()

    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[request(client) for i in range(N)])

    print(f"{time.time()-start:.2f}s")
    print(responses)

    async with httpx.AsyncClient() as client:
        response = await request_postgre(client)

    print(response.json())


if __name__ == '__main__':
    asyncio.run(main())
