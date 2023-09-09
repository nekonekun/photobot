from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from photobot.tg.routers.callbacks.user import UserSettings


def options_kb(locale: str | None = None) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=_('kb_options_language', locale=locale),
                callback_data=UserSettings(
                    field='language', value=None,
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def language_kb() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text='🇷🇺 Русский',
                callback_data=UserSettings(
                    field='language', value='ru',
                ).pack(),
            ),
            InlineKeyboardButton(
                text='🇺🇸/🇬🇧 English',
                callback_data=UserSettings(
                    field='language', value='en',
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
