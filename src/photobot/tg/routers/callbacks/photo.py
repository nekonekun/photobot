from aiogram.filters.callback_data import CallbackData


class PhotoCoords(CallbackData, prefix='ph_coords'):
    latitude: float
    longitude: float
