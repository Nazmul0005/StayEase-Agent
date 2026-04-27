from sqlalchemy.orm import Session
from com.app.database.models.models import Listing, Booking


def get_all_listings(db: Session) -> list[Listing]:
    """Returns all listings from the database."""
    return db.query(Listing).filter(Listing.is_available == True).all()


def get_booking_by_id(booking_id: str, db: Session) -> Booking | None:
    """Returns a booking by its UUID, or None if not found."""
    return db.query(Booking).filter(Booking.id == booking_id).first()