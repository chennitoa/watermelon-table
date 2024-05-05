from fastapi import APIRouter, HTTPException

from ..models import models
from ..services.db import listing_manager
from ..services.gmaps import gmaps_api


router = APIRouter(
    prefix='/listings',
    tags=['listings']
)


# Create new listing
@router.post("/")
def create_listing(listing: models.Listing):
    # Calculate the location first
    if listing.location is not None:
        try:
            lat, long = gmaps_api.geocode(listing.location)[0]['geometry']['location'].values()
        except Exception:
            return {
                "message:": f"Invalid location: {listing.location}.",
                "status": "failure"
            }
    else:
        lat, long = (None, None)

    status = listing_manager.create_listing(listing.username, listing.title,
                                            listing.description, lat, long, listing.location)

    if status:
        return {
            "message": f"New listing created for user {listing.username}.",
            "status": "success"
        }
    else:
        return {
            "message": f"Failed to create listing for user {listing.username}",
            "status": "failure"
        }


# Update an existing listing
@router.put("/update/")
def update_listing(update: models.UpdateListing):
    # Calculate the location first
    if update.location is not None:
        try:
            lat, long = gmaps_api.geocode(update.location)[0]['geometry']['location'].values()
        except Exception:
            return {
                "message:": f"Invalid location: {update.location}.",
                "status": "failure"
            }
    else:
        lat, long = (None, None)

    status = listing_manager.update_listing(update.listing_id, update.title,
                                            update.description, lat, long, update.location)

    if status:
        return {
            "message": f"Listing {update.listing_id} has been updated.",
            "status": "success"
        }
    else:
        return {
            "message": f"Failed to update listing {update.listing_id}.",
            "status": "failure"
        }


# Delete an existing listing
@router.delete("/delete/{listing_id}")
def delete_listing(listing_id: int):
    status = listing_manager.delete_listing(listing_id)

    if status:
        return {
            "message": f"Listing {listing_id} has been deleted.",
            "status": "success"
        }
    else:
        return {
            "message": f"Failed to delete listing {listing_id}",
            "status": "failure"
        }


@router.get("/get/{listing_id}")
def get_listing(listing_id: int):
    listing = listing_manager.get_listing(listing_id)

    if listing:
        return {
            "result": listing,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find listing.")


@router.post("/search/")
def search_listings(search: models.SearchListings):
    """Get an existing listing."""
    # Calculate the location first
    if search.location is not None:
        try:
            lat, long = gmaps_api.geocode(search.location)[0]['geometry']['location'].values()
        except Exception:
            return {
                "message:": f"Invalid location: {search.location}.",
                "status": "failure"
            }
    else:
        lat, long = (None, None)

    listings = listing_manager.search_listings(search.username, search.title,
                                               search.description, lat, long, search.distance)

    return {
        "result": listings,
        "status": "success"
    }
