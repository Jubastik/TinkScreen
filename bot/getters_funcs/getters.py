from aiogram_dialog import DialogManager


async def greetingGetter(dialog_manager: DialogManager, **kwargs):
    return {
        "name": dialog_manager.current_context().start_data["name"]
    }


async def respGetter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().dialog_data["resp"]
    results = data["results"]
    flag = False
    problem = {
        "manipulation": 'нет',
        "profanity": 'нет',
        "advertisement": 'нет',
        "begging": 'нет'
    }
    for i in results:
        print(i)
        if i["is_violation"]:
            flag = True
            problem[i["type"]["name"]] = i["violation"]
    if flag:
        flag = "Текст не прошёл проверку"
    else:
        flag = "Текст прошёл проверку"
    return {
        "result": flag,
        "violations": problem
    }