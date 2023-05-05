from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogRegistry, DialogManager, StartMode
from TOKENS import telegram_token
from api.api_functions import create_user, get_one_user
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Row, Column
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram.types import ContentType
from getters_funcs.getters import greetingGetter, respGetter
from methods import sendPost, sendtomanager, historyGroup, cleaner
from aiogram_dialog.widgets.input import MessageInput
from api.api_functions import check_text
from aiogram.dispatcher.filters.state import StatesGroup, State


storage = MemoryStorage()
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


async def historySwitching(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.history)


async def textAnalyze(message: Message, message_input: MessageInput, manager: DialogManager):
    resp = await check_text(message.from_user.id, message.text)
    await cleaner(manager)
    manager.current_context().dialog_data["resp"] = resp
    print(resp)
    await manager.dialog().switch_to(MySG.answer)


async def goback(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.main)


class MySG(StatesGroup):
    main = State()
    moder = State()
    history = State()
    answer = State()


dialog = Dialog(
    Window(
        Format("Здравствуйте, {name}!", ),
        Row(
            Button(Const("Отправить"), id="send", on_click=sendPost),
            Button(Const("История"), id="history", on_click=historySwitching),
        ),
        state=MySG.main,
        getter=greetingGetter,
    ),
    Window(
        Const("Пришлите текст на проверку"),
        Column(
            Button(Const("Назад"), id="back", on_click=goback),
            Button(Const("Допроверка"), id="sendToManager", on_click=sendtomanager)
        ),
        MessageInput(textAnalyze, content_types=[ContentType.TEXT]),
        state=MySG.moder,
    ),
    Window(
        Const("Вот история ваших отправок:"),
        historyGroup,
        state=MySG.history,
    ),
    Window(
        Multi(
            Format("{result}:"),
            Format("manipulation: {violations[manipulation]}"),
            Format("profanity: {violations[profanity]}"),
            Format("advertisement: {violations[advertisement]}"),
            Format("begging: {violations[begging]}"),
        ),
        Button(Const("Назад"), id="back", on_click=goback),
        state=MySG.answer,
        getter=respGetter
    )
)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    id = m.from_user.id
    name = m.from_user.first_name
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK, data={
        "name": name,
        "id": id
    })
    resp = await get_one_user(m.from_user.id)
    if 'detail' in resp:
        await create_user(name, id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)