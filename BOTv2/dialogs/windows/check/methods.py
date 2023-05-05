from random import choice

from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode

from dialogs.universal_methods import get_tg_id_from_manager, get_user
from services.restapi.restapi import api_check_text


async def finish_check(message: Message, dialog: DialogProtocol, manager: DialogManager, text_to_del=None):
    user = await get_user(get_tg_id_from_manager(manager))
    api_res = await api_check_text(user["tg_id"], manager.dialog_data["text"])
    check_text = [f"    <i>{str(api_res['text'][:150]) + '...' if len(api_res['text']) > 200 else api_res['text']}</i>\nОбнаруженные нарушения:"]
    for chk in api_res["results"]:
        if chk["is_violation"]:
            check_text.append(f"❗️Текст содержит {chk['type']['name']}: {chk['violation']}")
    if len(check_text) == 1:
        check_text.append("Нарушений не обнаружено 🎉")
    manager.dialog_data["check"] = "\n".join(check_text)
    if text_to_del:
        await text_to_del.delete()
    await manager.next()


async def getter_info(dialog_manager: DialogManager, **kwargs):
    return {"check": dialog_manager.dialog_data["check"]}


async def handle_text(message: Message, dialog: DialogProtocol, manager: DialogManager):
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    text = await message.answer("Проверка текста... Ожидайте")
    manager.dialog_data["text"] = message.text
    await finish_check(message, dialog, manager, text_to_del=text)
