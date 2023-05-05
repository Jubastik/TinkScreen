from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Start, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from dialogs.states import HistorySG, CheckSG, MenuSG
from dialogs.windows.check.methods import handle_text, getter_info
from dialogs.windows.history.methods import getter_history_main, start_history_info

HistoryMainWin = Window(
    Format("Выбери проверку 👇"),
    Group(
        ScrollingGroup(
            Select(Format("{item[text]}"), "history_btn", lambda res: res["id"], "checks",
                   on_click=start_history_info),
            width=2, height=5,
            id="history_group"),
        Cancel(Const("Меню")),
    ),
    state=HistorySG.main,
    getter=getter_history_main,
)
