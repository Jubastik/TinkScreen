from random import choice

from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol

from dialogs.universal_methods import get_tg_id_from_manager

stickers = ['👍', '👻', '😄', '🧐', '👀', '🌝', '🎫', '🔫', '📌', '📚']


async def getter_menu(dialog_manager: DialogManager, **kwargs):
    tg_id = get_tg_id_from_manager(dialog_manager)
    return {"name": "Имя",
            "sticker": choice(stickers),
            "not_btn_text": "Отключить уведомления" ,
            "not_text": "Уведомления включены ✅"}


async def change_notifications(message: Message, dialog: DialogProtocol, manager: DialogManager):
    tg_id = get_tg_id_from_manager(manager)
