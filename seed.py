"""
Seed script — populates the listings table with realistic Bangladeshi properties.
Run once after the database is created:
    python seed.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from com.app.database.db_connection.db_connection import SessionLocal, engine
from com.app.database.models.models import Base, Listing

Base.metadata.create_all(bind=engine)

LISTINGS = [
    # ── Cox's Bazar ────────────────────────────────────────────────────────────
    {
        "name": "Sea Pearl Beach Resort",
        "location": "Cox's Bazar",
        "address": "Kolatoli Beach Road, Cox's Bazar, Chittagong Division",
        "price_per_night": 4500.0,
        "max_guests": 4,
        "amenities": ["WiFi", "AC", "Sea View", "Breakfast Included", "Swimming Pool"],
        "photo_urls": ["https://example.com/seapearl1.jpg"],
        "house_rules": "No smoking indoors. Check-in after 2:00 PM. Check-out by 12:00 PM.",
        "is_available": True,
    },
    {
        "name": "Ocean Paradise Hotel",
        "location": "Cox's Bazar",
        "address": "Marine Drive Road, Cox's Bazar",
        "price_per_night": 3200.0,
        "max_guests": 3,
        "amenities": ["WiFi", "AC", "Ocean View", "Room Service"],
        "photo_urls": ["https://example.com/oceanparadise1.jpg"],
        "house_rules": "No parties. Quiet hours after 10 PM.",
        "is_available": True,
    },
    {
        "name": "Coral Reef Guest House",
        "location": "Cox's Bazar",
        "address": "Sugandha Beach, Cox's Bazar",
        "price_per_night": 1800.0,
        "max_guests": 2,
        "amenities": ["WiFi", "Fan", "Shared Bathroom", "Rooftop Access"],
        "photo_urls": ["https://example.com/coralreef1.jpg"],
        "house_rules": "No smoking. No outside food allowed.",
        "is_available": True,
    },
    {
        "name": "Blue Horizon Villa",
        "location": "Cox's Bazar",
        "address": "Inani Beach Road, Cox's Bazar",
        "price_per_night": 6800.0,
        "max_guests": 6,
        "amenities": ["WiFi", "AC", "Private Beach Access", "Full Kitchen", "Parking"],
        "photo_urls": ["https://example.com/bluehorizon1.jpg"],
        "house_rules": "No events or gatherings. Check-in after 3 PM.",
        "is_available": True,
    },

    # ── Dhaka ──────────────────────────────────────────────────────────────────
    {
        "name": "Gulshan Executive Apartment",
        "location": "Dhaka",
        "address": "Road 27, Gulshan 2, Dhaka 1212",
        "price_per_night": 5500.0,
        "max_guests": 3,
        "amenities": ["WiFi", "AC", "Fully Equipped Kitchen", "24hr Security", "Parking"],
        "photo_urls": ["https://example.com/gulshan1.jpg"],
        "house_rules": "No smoking. No pets. ID required at check-in.",
        "is_available": True,
    },
    {
        "name": "Banani Cozy Studio",
        "location": "Dhaka",
        "address": "Road 11, Banani, Dhaka 1213",
        "price_per_night": 2800.0,
        "max_guests": 2,
        "amenities": ["WiFi", "AC", "Kitchenette", "Smart TV"],
        "photo_urls": ["https://example.com/banani1.jpg"],
        "house_rules": "No loud music after 11 PM. No smoking.",
        "is_available": True,
    },
    {
        "name": "Dhanmondi Lake View Room",
        "location": "Dhaka",
        "address": "Road 8, Dhanmondi, Dhaka 1205",
        "price_per_night": 2200.0,
        "max_guests": 2,
        "amenities": ["WiFi", "AC", "Lake View", "Breakfast Included"],
        "photo_urls": ["https://example.com/dhanmondi1.jpg"],
        "house_rules": "Guests only. No visitors after 9 PM.",
        "is_available": True,
    },

    # ── Sylhet ─────────────────────────────────────────────────────────────────
    {
        "name": "Tea Garden Retreat",
        "location": "Sylhet",
        "address": "Srimangal Road, Sylhet Division",
        "price_per_night": 3500.0,
        "max_guests": 4,
        "amenities": ["WiFi", "AC", "Tea Garden View", "Breakfast Included", "Garden"],
        "photo_urls": ["https://example.com/teagarden1.jpg"],
        "house_rules": "No smoking. Children welcome. Check-out by 11 AM.",
        "is_available": True,
    },
    {
        "name": "Jaflong Riverside Cottage",
        "location": "Sylhet",
        "address": "Jaflong, Goainghat, Sylhet",
        "price_per_night": 2500.0,
        "max_guests": 5,
        "amenities": ["WiFi", "Fan", "River View", "BBQ Area", "Outdoor Seating"],
        "photo_urls": ["https://example.com/jaflong1.jpg"],
        "house_rules": "No alcohol. Family-friendly only.",
        "is_available": True,
    },

    # ── Bandarban ──────────────────────────────────────────────────────────────
    {
        "name": "Hill Top Resort Bandarban",
        "location": "Bandarban",
        "address": "Nilgiri Road, Bandarban Hill District",
        "price_per_night": 4000.0,
        "max_guests": 4,
        "amenities": ["WiFi", "AC", "Mountain View", "Restaurant", "Trekking Guide"],
        "photo_urls": ["https://example.com/hilltop1.jpg"],
        "house_rules": "No smoking indoors. Early check-in available on request.",
        "is_available": True,
    },
    {
        "name": "Meghla Guest House",
        "location": "Bandarban",
        "address": "Meghla Tourist Complex, Bandarban",
        "price_per_night": 1500.0,
        "max_guests": 3,
        "amenities": ["WiFi", "Fan", "Lake View", "Shared Kitchen"],
        "photo_urls": ["https://example.com/meghla1.jpg"],
        "house_rules": "No outside guests. Quiet after 10 PM.",
        "is_available": True,
    },

    # ── Sundarbans ─────────────────────────────────────────────────────────────
    {
        "name": "Mangrove Eco Lodge",
        "location": "Sundarbans",
        "address": "Mongla, Bagerhat, Khulna Division",
        "price_per_night": 3800.0,
        "max_guests": 6,
        "amenities": ["WiFi", "AC", "River View", "Boat Tour Included", "All Meals"],
        "photo_urls": ["https://example.com/mangrove1.jpg"],
        "house_rules": "No plastic. Eco-friendly stay. No loud noise (wildlife area).",
        "is_available": True,
    },
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Listing).count()
        if existing > 0:
            print(f"⚠️  Database already has {existing} listings. Skipping seed.")
            print("   To re-seed, delete all listings first:")
            print("   psql -d stayease -c 'DELETE FROM listings;'")
            return

        for data in LISTINGS:
            listing = Listing(**data)
            db.add(listing)

        db.commit()
        print(f"✅ Seeded {len(LISTINGS)} listings successfully.")
        print("\nLocations added:")
        locations = {}
        for l in LISTINGS:
            locations[l["location"]] = locations.get(l["location"], 0) + 1
        for loc, count in locations.items():
            print(f"   {loc}: {count} properties")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()