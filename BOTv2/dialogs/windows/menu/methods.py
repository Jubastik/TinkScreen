from random import choice

from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol

from dialogs.universal_methods import get_tg_id_from_manager, get_user

stickers = ['👍', '👻', '😄', '🧐', '👀', '🌝', '🎫', '🔫', '📌', '📚']


async def getter_menu(dialog_manager: DialogManager, **kwargs):
    user = await get_user(get_tg_id_from_manager(dialog_manager))
    return {"name": user["name"],
            "sticker": choice(stickers)}


