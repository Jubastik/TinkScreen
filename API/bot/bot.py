from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from TOKENS import telegram_token

storage = MemoryStorage()
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


class MySG(StatesGroup):
    main = State()


async def sendPost(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Принято!")


async def complain(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Вы пожаловались. Результат скоро будет.")


dialog = Dialog(
    Window(
        Format("Здравствуйте!"),
        Row(
            Button(Const("Проверить"), id="send", on_click=sendPost),
            Button(Const("Пожаловаться"), id="complain", on_click=complain),

        ),
        Button(Const("Что-то ещё"), id="nothing"),
        state=MySG.main,
    )
)
registry.register(dialog)

@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)