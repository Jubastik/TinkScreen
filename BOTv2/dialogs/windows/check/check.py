from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Start, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialogs.states import HistorySG, CheckSG, MenuSG
from dialogs.windows.check.methods import handle_text

CheckMainWin = Window(
    Format("Отправь текст для проверки 😉"),
    Group(
        Cancel(Const("Назад")),
    ),
    MessageInput(handle_text),
    state=CheckSG.main,
)

CheckInfoWin = Window(
    Format("Результат проверки 👇"),
    Group(
        Cancel(Const("Назад")),
    ),
    state=CheckSG.info,
)
