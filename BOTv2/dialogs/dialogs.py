import asyncio
import logging

from aiogram import Router
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent
from aiohttp import ClientConnectorError

from dialogs.states import MenuSG
from dialogs.universal_methods import login_user, del_message_by, del_keyboard
from dialogs.windows.bot_info.bot_info import InfoMainWin
from dialogs.windows.menu.menu import MenuMainWin
from dialogs.windows.registration.registration import RegMainWin, RegLoginWin
from dialogs.windows.removal_user.removal import RemovalMainWin
from dialogs.windows.subscriptions.subscriptions import SubscriptionsMainWin, SubscriptionsInfoWin
from my_errors import ApiError

dlg_router = Router()


@dlg_router.message(CommandStart())
async def handle_start_query(message: Message, dialog_manager: DialogManager):
    await get_user(message.from_user.id, message.from_user.first_name)
    await starting_dispatcher(message, dialog_manager)


async def starting_dispatcher(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuSG.main, mode=StartMode.RESET_STACK)


@dlg_router.message(Text(text="Вызвать меню"))
async def update_menu(message: Message, dialog_manager: DialogManager):
    await del_keyboard(message)
    await message.delete()
    await dialog_manager.show()


@dlg_router.message(Command("ping"))
async def handle_ping(message: Message):
    await message.reply("pong🟢")


async def error_handler(event, dialog_manager: DialogManager):
    logging.error(event.exception)
    if isinstance(event.exception, UnknownIntent):
        # Handling an error related to an outdated callback
        await handle_start_query(event.update.callback_query, dialog_manager)
    elif isinstance(event.exception, ApiError):
        # await starting_dispatcher(event.update.callback_query, dialog_manager)
        await event.update.callback_query.answer(
            "Ошибка сервера\n"
            "Вероятное решение проблемы - /start", show_alert=True)
    elif isinstance(event.exception, ClientConnectorError):
        await event.update.callback_query.answer("Сервер недоступен", show_alert=True)
    else:
        return UNHANDLED


# RegistrationDLG = Dialog(RegMainWin, RegLoginWin)
# InfoDLG = Dialog(InfoMainWin)
MenuDLG = Dialog(MenuMainWin)
# RemovalDLG = Dialog(RemovalMainWin)
# SubscriptionsDLG = Dialog(SubscriptionsMainWin, SubscriptionsInfoWin)
