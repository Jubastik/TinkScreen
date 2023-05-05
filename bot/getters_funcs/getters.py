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
    print(results)
    for i in results:
        print(i)
        if i["is_violation"]:
            flag = True
            print(i["type"])
            problem[i["type"]["name"]] = i["violation"]
        print(problem)
    if flag:
        flag = "Текст не прошёл проверку"
    else:
        flag = "Текст прошёл проверку"
    return {
        "result": flag,
        "violations": problem
    }