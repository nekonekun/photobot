from __future__ import annotations

from typing import Final

from geoalchemy2 import Geography
from geoalchemy2.elements import WKBElement
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


convention = {
    'ix': 'ix__%(column_0_label)s',
    'uq': 'uq__%(table_name)s__%(column_0_name)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': 'pk__%(table_name)s',
}
meta = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = meta


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(
        'telegram_id',
        BigInteger,
        primary_key=True,
        autoincrement=False,
    )
    language_code: Mapped[str] = mapped_column('language_code', String)
    photos: Mapped[list[Photo]] = relationship(back_populates='author')
    is_active: Mapped[bool] = mapped_column(
        'is_active',
        Boolean,
        server_default='true',
    )


photo_hashtag_association: Final[Table] = Table(
    'photos_hashtags',
    Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id'), primary_key=True),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'), primary_key=True),
)


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    hashtag: Mapped[str] = mapped_column('hashtag', String, unique=True)


class Photo(Base):
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(
        'id', Integer, primary_key=True, autoincrement=True,
    )
    file_id: Mapped[str] = mapped_column('file_id', String)
    author_id: Mapped[int] = mapped_column(
        'user_id',
        ForeignKey('users.telegram_id'),
        nullable=False,
    )
    author: Mapped[User] = relationship(back_populates='photos')
    description: Mapped[str] = mapped_column(
        'description',
        String,
        nullable=True,
    )
    location: Mapped[WKBElement] = mapped_column(
        'location',
        Geography(),
        nullable=True,
    )

    ht: Mapped[list[Hashtag]] = relationship(
        secondary=lambda: photo_hashtag_association,
    )

    hashtags: AssociationProxy[list[str]] = association_proxy(
        'ht',
        'hashtag',
    )
