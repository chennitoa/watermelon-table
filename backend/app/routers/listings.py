from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated

from .auth import oauth2_bearer
from ..models import models
from ..services.db import listing_manager, user_manager
from ..services.gmaps import gmaps_api
from ..services.oauth import decode_access_token


router = APIRouter(
    prefix='/listings',
    tags=['listings']
)


@router.post("/")
def create_listing(listing: models.Listing, token: Annotated[str, Depends(oauth2_bearer)]):
    """Create a new listing."""
    # Validate the token
    if decode_access_token(token) != listing.username:
        raise HTTPException(status_code=403, detail="Cannot create listing: authorization error.")

    # Calculate the location first
    if listing.location is not None:
        try:
            lat, long = gmaps_api.geocode(listing.location)[0]['geometry']['location'].values()
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid location: {listing.location}.")
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
        raise HTTPException(status_code=409, detail=f"Failed to create listing for user {listing.username}.")


@router.put("/update/")
def update_listing(update: models.UpdateListing, token: Annotated[str, Depends(oauth2_bearer)]):
    """Update an existing listing."""
    # Validate the token
    listing = listing_manager.get_listing(update.listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Invalid listing ID.")
    user = user_manager.get_user(listing["user_id"], is_username=False)

    if decode_access_token(token) != user["username"]:
        raise HTTPException(status_code=403, detail="Cannot update listing: authorization error.")

    # Calculate the location first
    if update.location is not None:
        try:
            lat, long = gmaps_api.geocode(update.location)[0]['geometry']['location'].values()
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid location: {update.location}.")
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
        raise HTTPException(status_code=409, detail=f"Failed to update listing {update.listing_id}.")


@router.delete("/delete/{listing_id}")
def delete_listing(listing_id: int, token: Annotated[str, Depends(oauth2_bearer)]):
    """Delete an existing listing."""
    # Validate the token
    listing = listing_manager.get_listing(listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Invalid listing ID.")
    user = user_manager.get_user(listing["user_id"], is_username=False)

    if decode_access_token(token) != user["username"]:
        raise HTTPException(status_code=403, detail="Cannot delete listing: authorization error.")

    status = listing_manager.delete_listing(listing_id)

    if status:
        return {
            "message": f"Listing {listing_id} has been deleted.",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Failed to delete listing {listing_id}.")


@router.get("/get/{listing_id}")
def get_listing(listing_id: int):
    listing = listing_manager.get_listing(listing_id)

    if listing:
        return {
            "result": listing,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Failed to find listing {listing_id}.")


@router.post("/search/")
def search_listings(search: models.SearchListings):
    """Get an existing listing."""
    # Calculate the location first
    if search.location is not None:
        try:
            lat, long = gmaps_api.geocode(search.location)[0]['geometry']['location'].values()
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid location: {search.location}.")

    else:
        lat, long = (None, None)

    listings = listing_manager.search_listings(search.username, search.title,
                                               search.description, lat, long, search.distance, search.rating)

    return {
        "result": listings,
        "status": "success"
    }
