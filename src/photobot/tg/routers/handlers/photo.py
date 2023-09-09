import logging

from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from photobot.application.photo.service import (
    PhotoCreate,
    PhotoDescriptionSet,
    PhotoHashtagFilter,
    PhotoHashtagsSet,
    PhotoLocationSet,
    PhotoService,
)
from photobot.tg.routers.callbacks.photo import PhotoCoords
from photobot.tg.routers.keyboards.photo import photo_result_kb, self_photo_kb
from photobot.tg.routers.states.photo import PhotoEdit

photo_router = Router()


@photo_router.message(F.photo & ~F.via_bot)
async def process_photo(
    message: types.Message,
    state: FSMContext,
    photo_service: PhotoService,
):
    logging.error(message)
    photo = await photo_service.add_photo(
        PhotoCreate(
            file_id=message.photo[0].file_id,
            author_id=message.from_user.id,
        ),
    )
    await state.update_data({'current_photo': photo.id})
    await state.set_state(PhotoEdit.editing)
    await message.answer(_('photo_accepted'), reply_markup=self_photo_kb())


@photo_router.message(F.location)
async def set_location(
    message: types.Message,
    state: FSMContext,
    photo_service: PhotoService,
):
    data = await state.get_data()
    photo_id = data['current_photo']
    await photo_service.set_photo_location(
        PhotoLocationSet(
            id=photo_id,
            latitude=message.location.latitude,
            longitude=message.location.longitude,
        ),
    )
    await message.answer(_('photo_location_set'))


@photo_router.message(PhotoEdit.editing)
async def read_description(
    message: types.Message,
    state: FSMContext,
    photo_service: PhotoService,
):
    description = message.text
    if message.entities:
        hashtags = [
            entity.extract_from(message.text)
            for entity in message.entities
            if entity.type == 'hashtag'
        ]
    else:
        hashtags = []
    data = await state.get_data()
    photo_id = data['current_photo']
    await photo_service.set_photo_description(
        PhotoDescriptionSet(id=photo_id, description=description),
    )
    await photo_service.set_photo_hashtags(
        PhotoHashtagsSet(id=photo_id, hashtags=hashtags),
    )
    await message.answer(_('photo_text_updated'))


@photo_router.inline_query(F.chat_type == 'sender')
async def query_photos(
    query: types.InlineQuery,
    photo_service: PhotoService,
):
    possible_hashtag = query.query
    if not possible_hashtag.startswith('#'):
        return []
    if query.location:
        photos = await photo_service.get_photos_by_hashtag(
            PhotoHashtagFilter(
                hashtag=possible_hashtag,
                latitude=query.location.latitude,
                longitude=query.location.longitude,
            ),
        )
    else:
        photos = await photo_service.get_photos_by_hashtag(
            PhotoHashtagFilter(
                hashtag=possible_hashtag,
            ),
        )
    inline_response = []
    for photo in photos:
        if photo.location:
            inline_response.append(
                types.InlineQueryResultCachedPhoto(
                    id=str(photo.id),
                    photo_file_id=photo.file_id,
                    caption=photo.description,
                    reply_markup=photo_result_kb(
                        photo.location.latitude,
                        photo.location.longitude,
                    ),
                ),
            )
        else:
            inline_response.append(
                types.InlineQueryResultCachedPhoto(
                    id=str(photo.id),
                    photo_file_id=photo.file_id,
                    caption=photo.description,
                ),
            )

    await query.answer(inline_response)
    return None


@photo_router.callback_query(PhotoCoords.filter())
async def show_photo_location(
    call: types.CallbackQuery, callback_data: PhotoCoords, bot: Bot,
):
    await call.answer()
    await bot.send_location(
        call.from_user.id,
        latitude=callback_data.latitude,
        longitude=callback_data.longitude,
    )
