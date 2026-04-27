from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class ListingResponse(BaseModel):
    """Public representation of a property listing."""
    id: UUID
    name: str
    location: str
    address: Optional[str]
    price_per_night: float = Field(..., description="Price per night in BDT")
    max_guests: int
    amenities: list[str]
    photo_urls: list[str]
    house_rules: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True


class BookingResponse(BaseModel):
    """Public representation of a confirmed booking."""
    id: UUID
    listing_id: UUID
    guest_name: str
    guest_phone: Optional[str]
    check_in: date
    check_out: date
    guests: int
    total_price: float = Field(..., description="Total price in BDT")
    status: str
    created_at: datetime

    class Config:
        from_attributes = True