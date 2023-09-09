from dataclasses import dataclass


@dataclass
class PhotoCreate:
    file_id: str
    author_id: int


@dataclass
class PhotoLocationSet:
    id: int
    latitude: float
    longitude: float


@dataclass
class PhotoDescriptionSet:
    id: int
    description: str


@dataclass
class PhotoHashtagsSet:
    id: int
    hashtags: list[str]


@dataclass
class PhotoHashtagFilter:
    hashtag: str
    latitude: float | None = None
    longitude: float | None = None


@dataclass
class PhotoAuthorFilter:
    telegram_id: int
