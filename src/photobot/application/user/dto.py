from dataclasses import dataclass


@dataclass
class UserCreate:
    telegram_id: int
    language_code: str


@dataclass
class UserSetActive:
    telegram_id: int
    is_active: bool


@dataclass
class UserSetLanguage:
    telegram_id: int
    language_code: str


@dataclass
class UserRead:
    telegram_id: int
