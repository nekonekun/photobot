from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    language_code: str
    is_active: bool
