import asyncio
import aiohttp
import time

URL = "http://192.168.1.31:80/ds7-run-now-tan-test"  # URL server bạn muốn fetch

async def fetch(session, idx):
    start = time.perf_counter()
    async with session.post(
        URL,
        json={
            "prompt": "1234",
            "ai_api_key": "1234",
            "chat_ai_model": "1234"
        }
    ) as response:
        text = await response.text()
        elapsed = time.perf_counter() - start
        print(f"[{idx}] Status: {response.status} | Time: {elapsed:.2f} s")
        return text

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i) for i in range(1, 1000)]  # 100 request song song
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

if __name__ == "__main__":
    asyncio.run(main())
