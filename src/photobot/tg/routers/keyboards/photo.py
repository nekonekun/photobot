from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from photobot.tg.routers.callbacks.photo import PhotoCoords


def self_photo_kb():
    keyboard = [
        [
            KeyboardButton(
                text=_('kb_location_request'),
                request_location=True,
            ),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True,
    )


def photo_result_kb(latitude: float, longitude: float):
    keyboard = [
        [
            InlineKeyboardButton(
                text='Show location',
                callback_data=PhotoCoords(
                    latitude=latitude, longitude=longitude,
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
