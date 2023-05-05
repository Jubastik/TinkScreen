from random import choice

from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode

from dialogs.universal_methods import get_tg_id_from_manager, get_user


async def finish_check(message: Message, dialog: DialogProtocol, manager: DialogManager):
    user = await get_user(get_tg_id_from_manager(manager))
    print(manager.dialog_data["text"])
    manager.dialog_data["check"] = "ok"
    await manager.next()


async def handle_text(message: Message, dialog: DialogProtocol, manager: DialogManager):
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    manager.dialog_data["text"] = message.text
    await finish_check(message, dialog, manager)
