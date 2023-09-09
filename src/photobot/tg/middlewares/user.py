from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from photobot.application.user.service import UserService


class UserServiceMiddleware(BaseMiddleware):
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
            data['user_service'] = UserService(db_session=session)
            response = await handler(event, data)
            await session.commit()
            return response
