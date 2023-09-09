from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from photobot.entities import Author, Location, Photo
from photobot.infrastructure.database import models


class PhotoGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, file_id: str, author_id: int):
        new_photo = models.Photo(file_id=file_id, author_id=author_id)
        self.session.add(new_photo)
        await self.session.flush([new_photo])
        return Photo(
            id=new_photo.id,
            file_id=new_photo.file_id,
            description=None,
            location=None,
            author=Author(telegram_id=new_photo.author_id),
            hashtags=[],
        )

    async def update(
        self,
        id: int,
        description: str | None = None,
        hashtags: list[str] | None = None,
        location: tuple[float, float] | None = None,
    ):
        stmt = select(models.Photo)
        stmt = stmt.where(models.Photo.id == id)
        stmt = stmt.options(selectinload(models.Photo.ht))
        response = await self.session.execute(stmt)
        photo: models.Photo = response.scalars().first()
        if description is not None:
            photo.description = description
        if location is not None:
            wkt_string = f'POINT({location[1]} {location[0]})'
            photo.location = WKTElement(wkt_string, srid=4326)
        if hashtags is not None:
            stmt = select(models.Hashtag)
            stmt = stmt.where(models.Hashtag.hashtag.in_(hashtags))
            response = await self.session.execute(stmt)
            hashtag_objs = response.scalars().all()
            photo.ht = hashtag_objs
            await self.session.flush([photo])
        result = Photo(
            id=photo.id,
            file_id=photo.file_id,
            description=None,
            location=None,
            author=Author(telegram_id=photo.author_id),
            hashtags=photo.hashtags,
        )
        if photo.location:
            coords = to_shape(photo.location)
            result.location = Location(latitude=coords.y, longitude=coords.x)
        return result

    async def filter(
        self,
        center: tuple[float, float] | None = None,
        hashtag: str | None = None,
        limit: int = 5,
        offset: int = 0,
    ):
        stmt = select(models.Photo)
        if hashtag:
            stmt = stmt.where(models.Photo.hashtags == hashtag)
        if center:
            center = WKTElement(f'POINT({center[1]} {center[0]})', srid=4326)
            stmt = stmt.order_by(
                func.st_distance(models.Photo.location, center),
            )
        stmt = stmt.options(selectinload(models.Photo.author))
        stmt = stmt.options(selectinload(models.Photo.ht))
        stmt = stmt.offset(offset).limit(limit)
        response = await self.session.execute(stmt)
        result = []
        for photo in response.scalars().all():
            another_photo = Photo(
                id=photo.id,
                file_id=photo.file_id,
                description=photo.description,
                location=None,
                author=Author(telegram_id=photo.author_id),
                hashtags=photo.hashtags,
            )
            if photo.location:
                coords = to_shape(photo.location)
                another_photo.location = Location(
                    latitude=coords.y, longitude=coords.x,
                )
            result.append(another_photo)
        return result
