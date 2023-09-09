from aiogram.filters.callback_data import CallbackData


class UserSettings(CallbackData, prefix='settings'):
    field: str
    value: str | None
