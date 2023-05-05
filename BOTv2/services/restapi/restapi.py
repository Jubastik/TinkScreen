import aiohttp

from my_errors import ApiError, TOKEN_ERROR, USER_EXISTS, USER_ERROR
from schemas.resources_pdc import Resource
from services.restapi.URLS import URL_GET_JWT, URL_GET_MY_RESOURCES_UUIDS, URL_GET_RESOURCE, URL_DELETE_USER, URL_USER
from services.restapi.scripts import get_headers


async def api_create_user(tg_id: int, name: str):
    headers = await get_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        body = {
            "id": str(tg_id),
            "name": name,
        }
        async with session.post(URL_USER, json=body) as resp:
            data = await resp.json()
            if resp.status != 200 and data["error_code"] == 1101:
                raise ApiError(USER_EXISTS)
            if resp.status != 200:
                raise ApiError(USER_ERROR)
            return data

async def api_get_user(tg_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL_USER}/{str(tg_id)}") as resp:
            data = await resp.json()
            if resp.status != 200 and data["error_code"] == 1101:
                raise ApiError(USER_EXISTS)
            if resp.status != 200:
                raise ApiError(USER_ERROR)
            return data









async def api_get_my_resources_uuids(tg_id: int) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_GET_MY_RESOURCES_UUIDS, headers=await get_headers(tg_id)) as resp:
            if resp.status != 200:
                raise ApiError(TOKEN_ERROR)
            data = await resp.json()
            return [resource["resource_uuid"] for resource in data if resource["to_telegram"] is True]


async def api_get_resources(uuids: list) -> list[Resource]:
    async with aiohttp.ClientSession() as session:
        resources = []
        for uuid in uuids:
            async with session.get(f"{URL_GET_RESOURCE}/{uuid}", headers=await get_headers()) as resp:
                if resp.status != 200:
                    raise ApiError(TOKEN_ERROR)
                data = await resp.json()
                resources.append(Resource(**data))
        return resources


async def api_delete_user(tg_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL_DELETE_USER, headers=await get_headers(tg_id)) as resp:
            return True