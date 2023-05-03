from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row, Column, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format
from TOKENS import telegram_token
from aiogram_dialog.widgets.input import MessageInput

storage = MemoryStorage()
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


async def sendPost(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()


async def historySwitching(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.history)


async def getData(dialog_manager: DialogManager, **kwargs):
    return {
        "name": dialog_manager.current_context().start_data
    }


async def textAnalyze(message: Message, message_input: MessageInput, manager: DialogManager):
    text = message.text
    print(text)
    await manager.dialog().back()


async def other_type(message: Message, message_input: MessageInput,
                             manager: DialogManager):
    await message.answer("Text is expected")


async def goback(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().back()


async def sendtomanager(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Ваше сообщение отправлено на допроверку модератора")


def buttons_creator(btn_quantity):
    buttons = []
    for i in btn_quantity:
        i = str(i)
        buttons.append(Button(Const(i), id=i, on_click=historyClicked))
    return buttons


test_buttons = buttons_creator(range(0, 15))
historyGroup = ScrollingGroup(
            *test_buttons,
            id="numbers",
            width=6,
            height=2,
        )


class MySG(StatesGroup):
    main = State()
    moder = State()
    history = State()


dialog = Dialog(
    Window(
        Format("Здравствуйте, {name}!", ),
        Row(
            Button(Const("Отправить"), id="send", on_click=sendPost),
            Button(Const("История"), id="history", on_click=historySwitching),
        ),
        state=MySG.main,
        getter=getData,
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
)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK, data=m.from_user.first_name)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)