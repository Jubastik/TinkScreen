from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode, StartMode

from dialogs.states import RegistrationSG
from dialogs.universal_methods import get_tg_id_from_manager
from services.restapi.restapi import api_delete_user


async def delete_user(message: Message, dialog: DialogProtocol, manager: DialogManager):
    tg_id = get_tg_id_from_manager(manager)
    await api_delete_user(tg_id)
    await manager.start(RegistrationSG.main, show_mode=ShowMode.EDIT, mode=StartMode.RESET_STACK)
