from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start, Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.states import HistorySG, CheckSG, MenuSG
from dialogs.windows.menu.methods import getter_menu

MenuMainWin = Window(
    Format("Привет {name} {sticker}"),
    Group(
        Start(Const("История"), state=HistorySG.main, id="history_btn"),
        Start(Const("Проверка"), state=CheckSG.main, id="check_user_btn"),
        width=2,
    ),
    getter=getter_menu,
    state=MenuSG.main,
)
