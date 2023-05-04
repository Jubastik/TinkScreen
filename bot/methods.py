from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup


async def sendPost(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()


async def sendtomanager(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Ваше сообщение отправлено на допроверку модератора")


def buttons_creator(btn_quantity):
    buttons = []
    for i in btn_quantity:
        i = str(i)
        #buttons.append(Button(Const(i), id=i, on_click=historyClicked))
    return buttons


test_buttons = buttons_creator(range(0, 15))
historyGroup = ScrollingGroup(
            *test_buttons,
            id="numbers",
            width=6,
            height=2,
        )