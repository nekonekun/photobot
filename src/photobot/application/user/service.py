from sqlalchemy.ext.asyncio import AsyncSession

from photobot.application.exceptions import AppError
from photobot.application.user.dto import (
    UserCreate,
    UserRead,
    UserSetActive,
    UserSetLanguage,
)
from photobot.entities import User
from photobot.infrastructure.database.gateway.exceptions import GatewayError
from photobot.infrastructure.database.gateway.user import UserGateway


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.gateway = UserGateway(session=db_session)

    async def create_user(self, data: UserCreate) -> User:
        try:
            new_user = await self.gateway.create(
                telegram_id=data.telegram_id,
                language_code=data.language_code,
            )
        except GatewayError as error:
            raise AppError(str(error)) from error
        return new_user

    async def read_user(self, data: UserRead) -> User | None:
        try:
            user = await self.gateway.read(telegram_id=data.telegram_id)
        except GatewayError:
            return None
        return user

    async def set_active_status(self, data: UserSetActive) -> User:
        try:
            user = await self.gateway.update(
                telegram_id=data.telegram_id,
                is_active=data.is_active,
            )
        except GatewayError as error:
            raise AppError(str(error)) from error
        return user

    async def change_language(self, data: UserSetLanguage) -> User:
        try:
            user = await self.gateway.update(
                telegram_id=data.telegram_id,
                language_code=data.language_code,
            )
        except GatewayError as error:
            raise AppError(str(error)) from error
        return user
