from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class EventFrequency(StrEnum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class ActivityGroup(BaseModel):
    name: str
    category: str
    description: str
    founding_date: Optional[str]
    website: str
    email: Optional[str]
    phone_number: str
    social_media_links: str  # Json string
    is_active: bool
    total_members: int
    event_frequency: EventFrequency
    membership_fee: int
    open_to_public: bool
    min_age: int
