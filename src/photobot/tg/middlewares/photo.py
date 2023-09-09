from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from photobot.application.photo.service import PhotoService


class PhotoServiceMiddleware(BaseMiddleware):
    def __init__(self, pool: async_sessionmaker):
        super().__init__()
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.pool() as session:
            data['photo_service'] = PhotoService(db_session=session)
            try:
                await handler(event, data)
            except Exception:
                await session.rollback()
                raise
            else:
                await session.commit()
