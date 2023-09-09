from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from photobot.infrastructure.database import models


class HashtagGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ensure_existence(
        self,
        hashtag: str,
    ):
        stmt = insert(models.Hashtag)
        stmt = stmt.values(hashtag=hashtag)
        stmt = stmt.on_conflict_do_nothing()
        await self.session.execute(stmt)
        await self.session.commit()
