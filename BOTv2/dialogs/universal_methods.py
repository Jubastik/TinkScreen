from asyncio import sleep

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager

from my_errors import ApiError, USER_EXISTS
from services.restapi.restapi import api_create_user, api_get_user


def get_tg_id_from_manager(dialog_manager: DialogManager):
    return dialog_manager.middleware_data["event_from_user"].id


async def del_message_by(message, seconds):
    await sleep(seconds)
    await message.delete()


async def get_user(tg_id: int, name: str | None = None):
    try:
        user = await api_create_user(tg_id, name)
    except ApiError as e:
        if e.error_code == USER_EXISTS:
            user = await api_get_user(tg_id)
        else:
            raise e
    return user


