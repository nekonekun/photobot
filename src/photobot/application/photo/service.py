from sqlalchemy.ext.asyncio import AsyncSession

from photobot.application.photo.dto import (
    PhotoCreate,
    PhotoDescriptionSet,
    PhotoHashtagFilter,
    PhotoHashtagsSet,
    PhotoLocationSet,
)
from photobot.entities import Photo
from photobot.infrastructure.database.gateway.hashtag import HashtagGateway
from photobot.infrastructure.database.gateway.photo import PhotoGateway


class PhotoService:
    def __init__(self, db_session: AsyncSession):
        self.gateway = PhotoGateway(session=db_session)
        self.hashtag_gateway = HashtagGateway(session=db_session)

    async def add_photo(self, data: PhotoCreate) -> Photo:
        return await self.gateway.create(
            file_id=data.file_id, author_id=data.author_id,
        )

    async def set_photo_location(self, data: PhotoLocationSet) -> Photo:
        return await self.gateway.update(
            id=data.id,
            location=(data.latitude, data.longitude),
        )

    async def ensure_hashtags(self, *hashtags: str) -> None:
        for hashtag in hashtags:
            await self.hashtag_gateway.ensure_existence(hashtag)

    async def set_photo_hashtags(self, data: PhotoHashtagsSet) -> Photo:
        await self.ensure_hashtags(*data.hashtags)
        return await self.gateway.update(
            id=data.id,
            hashtags=data.hashtags,
        )

    async def set_photo_description(self, data: PhotoDescriptionSet) -> Photo:
        return await self.gateway.update(
            id=data.id,
            description=data.description,
        )

    async def get_photos_by_hashtag(
        self, data: PhotoHashtagFilter,
    ) -> list[Photo]:
        if data.latitude and data.longitude:
            return await self.gateway.filter(
                hashtag=data.hashtag, center=(data.latitude, data.longitude),
            )
        return await self.gateway.filter(hashtag=data.hashtag)

    async def get_photos_by_author_id(self) -> list[Photo]:
        pass
