import asyncio
import os
import pathlib

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from photobot.tg.middlewares.photo import PhotoServiceMiddleware
from photobot.tg.middlewares.user import UserServiceMiddleware
from photobot.tg.routers import photo_router, user_router

i18n = I18n(
    path=pathlib.Path(__file__).parent / 'locales',
    default_locale='en',
    domain='messages',
)


async def main():
    engine = create_async_engine(os.getenv('NPB_DB_URL'))
    pool = async_sessionmaker(bind=engine)
    user_service_middleware = UserServiceMiddleware(pool=pool)
    photo_service_middleware = PhotoServiceMiddleware(pool=pool)

    user_router.message.middleware.register(user_service_middleware)
    user_router.callback_query.middleware.register(user_service_middleware)

    photo_router.message.middleware.register(photo_service_middleware)
    photo_router.callback_query.middleware.register(photo_service_middleware)
    photo_router.inline_query.middleware.register(photo_service_middleware)

    bot = Bot(token=os.getenv('NPB_TOKEN'))
    dp = Dispatcher(storage=RedisStorage.from_url(os.getenv('NPB_REDIS_URL')))

    i18n_middleware = FSMI18nMiddleware(i18n)
    dp.message.outer_middleware.register(i18n_middleware)
    dp.callback_query.outer_middleware.register(i18n_middleware)

    dp.include_router(user_router)
    dp.include_router(photo_router)

    await dp.start_polling(bot)


def run():
    asyncio.run(main())


if __name__ == '__main__':
    run()
