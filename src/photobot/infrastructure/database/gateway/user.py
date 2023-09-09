from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from photobot.entities import User
from photobot.infrastructure.database import models
from photobot.infrastructure.database.gateway.exceptions import GatewayError


class UserGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        telegram_id: int,
        language_code: str,
    ):
        new_user = models.User(
            telegram_id=telegram_id,
            language_code=language_code,
        )
        try:
            self.session.add(new_user)
            await self.session.flush((new_user,))
        except IntegrityError as error:
            msg = 'Duplicate telegram_id'
            raise GatewayError(msg) from error
        return User(
            telegram_id=new_user.telegram_id,
            language_code=new_user.language_code,
            is_active=new_user.is_active,
        )

    async def update(
        self,
        telegram_id: int,
        language_code: str | None = None,
        is_active: bool | None = None,
    ):
        stmt = select(models.User).where(
            models.User.telegram_id == telegram_id,
        )
        response = await self.session.execute(stmt)
        user: models.User = response.scalars().first()
        if not user:
            msg = f'User with telegram_id {telegram_id} does not exist'
            raise GatewayError(msg)
        if language_code is not None:
            user.language_code = language_code
        if is_active is not None:
            user.is_active = is_active
        await self.session.flush((user,))
        return User(
            telegram_id=user.telegram_id,
            language_code=user.language_code,
            is_active=user.is_active,
        )

    async def read(self, telegram_id: int):
        stmt = select(models.User).where(
            models.User.telegram_id == telegram_id,
        )
        response = await self.session.execute(stmt)
        user: models.User = response.scalars().first()
        if not user:
            msg = f'User with telegram_id {telegram_id} does not exist'
            raise GatewayError(msg)
        return User(
            telegram_id=user.telegram_id,
            language_code=user.language_code,
            is_active=user.is_active,
        )
