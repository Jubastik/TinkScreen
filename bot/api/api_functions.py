import aiohttp
from bot.api.URLS import BASE_URL, GET_USER_URL, CHECK_URL


async def api_func():
    headers = {"access_token": "no"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL) as resp:
            data = await resp.json()
            print(data)


async def create_user(name, id):
    headers = {"access_token": "no"}
    body = {
        "name": name,
        "tg_id": id
    }
    print(body)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(GET_USER_URL, json=body) as resp:
            data = await resp.json()
            print(data)


async def get_one_user(id):
    headers = {"access_token": "no"}
    params = {
        "obj_id": id,
        "id_type": "student_tg"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(GET_USER_URL + str(id) + "?student_tg", params=params) as resp:
            data = await resp.json()
            print(data)
            return data


async def check_text(id, text):
    headers = {"access_token": "no"}
    body = {
        "text": text,
        "tg_id": id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(CHECK_URL, json=body) as resp:
            data = await resp.json()
            return data