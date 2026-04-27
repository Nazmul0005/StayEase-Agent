import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, Integer, Float, Boolean,
    DateTime, Date, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from com.app.database.db_connection.db_connection import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    price_per_night = Column(Float, nullable=False)          # in BDT
    max_guests = Column(Integer, nullable=False)
    amenities = Column(JSONB, default=list)                  # ["WiFi", "AC", ...]
    photo_urls = Column(JSONB, default=list)
    house_rules = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="listing")

    def __repr__(self) -> str:
        return f"<Listing id={self.id} name={self.name} location={self.location}>"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    guest_name = Column(String(255), nullable=False)
    guest_phone = Column(String(20), nullable=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    guests = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)              # in BDT
    status = Column(String(50), default="confirmed")         # confirmed / cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing", back_populates="bookings")

    def __repr__(self) -> str:
        return f"<Booking id={self.id} guest={self.guest_name} listing={self.listing_id}>"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(255), primary_key=True)               # conversation_id from client
    messages = Column(JSONB, default=list)                   # [{role, content, timestamp}]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Conversation id={self.id}>"