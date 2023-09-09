from dataclasses import dataclass


@dataclass
class Author:
    telegram_id: int


@dataclass
class Hashtag:
    hashtag: str


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class Photo:
    id: int
    file_id: str
    description: str | None
    location: Location | None
    author: Author
    hashtags: list[str]
