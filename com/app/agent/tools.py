from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from sqlalchemy.orm import Session

from com.app.database.models.models import Listing, Booking
from com.app.database.db_connection.db_connection import SessionLocal


# ─── Input Schemas ────────────────────────────────────────────────────────────

class SearchPropertiesInput(BaseModel):
    location: str = Field(description="City or area name, e.g. 'Cox's Bazar'")
    check_in: Optional[str] = Field(default=None, description="Check-in date in YYYY-MM-DD format")
    check_out: Optional[str] = Field(default=None, description="Check-out date in YYYY-MM-DD format")
    guests: Optional[int] = Field(default=1, description="Number of guests", ge=1, le=20)


class GetListingDetailsInput(BaseModel):
    listing_id: str = Field(description="UUID of the listing to fetch details for")


class CreateBookingInput(BaseModel):
    listing_id: str = Field(description="UUID of the listing to book")
    guest_name: str = Field(description="Full name of the guest")
    guest_phone: Optional[str] = Field(default=None, description="Guest contact number")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    guests: int = Field(description="Number of guests", ge=1)


# ─── Tools ────────────────────────────────────────────────────────────────────

@tool("search_available_properties", args_schema=SearchPropertiesInput)
def search_available_properties(
    location: str,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None,
    guests: int = 1,
) -> dict:
    """
    Search for available listings in a given location for specified dates and guest count.
    Returns a list of matching properties with id, name, price per night, and max guests.
    Used when the guest provides location, dates, and number of guests.
    """
    db: Session = SessionLocal()
    try:
        # Replace spaces with % to flexibly match "cox bazar" to "Cox's Bazar"
        flexible_location = location.replace(" ", "%")
        
        results = (
            db.query(Listing)
            .filter(
                Listing.location.ilike(f"%{flexible_location}%"),
                Listing.max_guests >= guests,
                Listing.is_available == True,
            )
            .all()
        )

        properties = [
            {
                "id": str(listing.id),
                "name": listing.name,
                "location": listing.location,
                "price_per_night": listing.price_per_night,
                "max_guests": listing.max_guests,
                "amenities": listing.amenities,
            }
            for listing in results
        ]

        return {
            "status": "success",
            "count": len(properties),
            "properties": properties,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@tool("get_listing_details", args_schema=GetListingDetailsInput)
def get_listing_details(listing_id: str) -> dict:
    """
    Fetch full details of a specific listing by its UUID.
    Returns name, location, address, price, amenities, photo URLs, and house rules.
    Used when the guest asks for more information about a specific property.
    """
    db: Session = SessionLocal()
    try:
        import uuid
        try:
            val = uuid.UUID(listing_id)
            listing = db.query(Listing).filter(Listing.id == val).first()
        except ValueError:
            listing = db.query(Listing).filter(Listing.name.ilike(f"%{listing_id}%")).first()

        if not listing:
            return {"status": "error", "message": "Listing not found"}

        return {
            "status": "success",
            "listing": {
                "id": str(listing.id),
                "name": listing.name,
                "location": listing.location,
                "address": listing.address,
                "price_per_night": listing.price_per_night,
                "max_guests": listing.max_guests,
                "amenities": listing.amenities,
                "photo_urls": listing.photo_urls,
                "house_rules": listing.house_rules,
                "is_available": listing.is_available,
            },
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@tool("create_booking", args_schema=CreateBookingInput)
def create_booking(
    listing_id: str,
    guest_name: str,
    check_in: str,
    check_out: str,
    guests: int,
    guest_phone: Optional[str] = None,
) -> dict:
    """
    Create a confirmed booking for a listing.
    Calculates total price based on number of nights and price per night.
    Returns booking ID, total price in BDT, and confirmation status.
    Used when the guest confirms they want to book a specific property.
    """
    db: Session = SessionLocal()
    try:
        import uuid
        try:
            val = uuid.UUID(listing_id)
            listing = db.query(Listing).filter(Listing.id == val).first()
        except ValueError:
            listing = db.query(Listing).filter(Listing.name.ilike(f"%{listing_id}%")).first()

        if not listing:
            return {"status": "error", "message": "Listing not found"}

        if not listing.is_available:
            return {"status": "error", "message": "Listing is not available"}

        check_in_date = date.fromisoformat(check_in)
        check_out_date = date.fromisoformat(check_out)
        nights = (check_out_date - check_in_date).days

        if nights <= 0:
            return {"status": "error", "message": "Check-out must be after check-in"}

        total_price = nights * listing.price_per_night

        booking = Booking(
            listing_id=listing.id,
            guest_name=guest_name,
            guest_phone=guest_phone,
            check_in=check_in_date,
            check_out=check_out_date,
            guests=guests,
            total_price=total_price,
            status="confirmed",
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "booking": {
                "booking_id": str(booking.id),
                "listing_name": listing.name,
                "guest_name": booking.guest_name,
                "check_in": check_in,
                "check_out": check_out,
                "nights": nights,
                "guests": guests,
                "total_price_bdt": total_price,
                "status": booking.status,
            },
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


# All tools exported for graph binding
TOOLS = [search_available_properties, get_listing_details, create_booking]