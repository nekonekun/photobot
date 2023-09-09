from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from photobot.application.user import (
    UserCreate,
    UserRead,
    UserService,
    UserSetLanguage,
)
from photobot.tg.routers.callbacks.user import UserSettings
from photobot.tg.routers.keyboards.user import language_kb, options_kb

user_router = Router()


@user_router.message(Command(commands=['start']))
async def start(
    message: types.Message,
    state: FSMContext,
    user_service: UserService,
):
    user = await user_service.read_user(
        UserRead(telegram_id=message.from_user.id),
    )
    if not user:
        user = await user_service.create_user(
            UserCreate(
                telegram_id=message.from_user.id,
                language_code=message.from_user.language_code,
            ),
        )
    await state.update_data({'locale': user.language_code})
    await message.answer(_('greeting_message_alt'))


@user_router.message(Command(commands=['options', 'settings']))
async def options(message: types.Message):
    await message.answer(_('option_menu_message'), reply_markup=options_kb())


@user_router.callback_query(UserSettings.filter(F.field == 'language'))
async def options_language(
    call: types.CallbackQuery,
    state: FSMContext,
    callback_data: UserSettings,
    user_service: UserService,
):
    await call.answer()
    if not callback_data.value:
        await call.message.edit_text(
            _('option_language_ask'),
            reply_markup=language_kb(),
        )
        return
    new_language = callback_data.value
    user = await user_service.change_language(
        UserSetLanguage(
            telegram_id=call.from_user.id,
            language_code=new_language,
        ),
    )
    await state.update_data({'locale': user.language_code})
    await call.message.edit_text(
        _('option_language_set', locale=new_language),
        reply_markup=options_kb(locale=new_language),
    )
