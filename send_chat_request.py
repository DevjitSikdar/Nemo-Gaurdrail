import asyncio
import aiohttp

async def send_request():
    url = "http://localhost:8000/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"message": "a" * 101}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()  # Raise an exception for bad status codes
                data = await response.json()
                print("Response:", data)
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(send_request())