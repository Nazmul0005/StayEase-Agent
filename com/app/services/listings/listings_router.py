from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from com.app.database.db_connection.db_connection import get_db
from com.app.services.listings.listings import get_all_listings, get_booking_by_id
from com.app.services.listings.listings_schema import ListingResponse, BookingResponse

router = APIRouter(prefix="/api/listings", tags=["Listings"])


@router.get(
    "/",
    response_model=list[ListingResponse],
    summary="Get all available listings",
)
def list_all_listings(db: Session = Depends(get_db)) -> list[ListingResponse]:
    """Returns all currently available property listings."""
    return get_all_listings(db)


@router.get(
    "/bookings/{booking_id}",
    response_model=BookingResponse,
    summary="Get a booking by ID",
)
def get_booking(booking_id: str, db: Session = Depends(get_db)) -> BookingResponse:
    """Returns a single booking by its UUID."""
    booking = get_booking_by_id(booking_id, db)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking