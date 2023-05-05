from random import choice

from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode

from dialogs.universal_methods import get_tg_id_from_manager, get_user
from services.restapi.restapi import api_check_text, api_get_checks


async def finish_check(message: Message, dialog: DialogProtocol, manager: DialogManager, text_to_del=None):
    user = await get_user(get_tg_id_from_manager(manager))
    api_res = await api_check_text(user["tg_id"], manager.dialog_data["text"])
    check_text = ["Обнаруженные нарушения:"]
    for chk in api_res["results"]:
        if chk["is_violation"]:
            check_text.append(f"❗️Текст содержит {chk['type']['name']}: {chk['violation']}")
    if len(check_text) == 1:
        check_text.append("Нарушений не обнаружено 🎉")
    manager.dialog_data["check"] = "\n".join(check_text)
    if text_to_del:
        await text_to_del.delete()
    await manager.next()


async def getter_history_main(dialog_manager: DialogManager, **kwargs):
    user = await get_user(get_tg_id_from_manager(dialog_manager))
    checks = await api_get_checks(user["tg_id"])
    return {"checks": checks}


async def start_history_info(message: Message, dialog: DialogProtocol, manager: DialogManager, check_id: int):
    user = await get_user(get_tg_id_from_manager(manager))
    api_res = await api_get_checks(user["tg_id"])
    my_res = None
    for res in api_res:
        if int(res["id"]) == int(check_id):
            my_res = res.copy()
            break
    check_text = ["Обнаруженные нарушения:"]
    for chk in my_res["results"]:
        if chk["is_violation"]:
            check_text.append(f"❗️Текст содержит {chk['type']['name']}: {chk['violation']}")
    if len(check_text) == 1:
        check_text.append("Нарушений не обнаружено 🎉")
    manager.dialog_data["check"] = "\n".join(check_text)
    await manager.next()
