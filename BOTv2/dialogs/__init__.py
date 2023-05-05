from aiogram_dialog import DialogRegistry

from dialogs.dialogs import MenuDLG, CheckDLG, HistoryDLG


def register_dialogs(registry: DialogRegistry):
    registry.register(MenuDLG)
    registry.register(CheckDLG)
    registry.register(HistoryDLG)


