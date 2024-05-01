from fastapi import APIRouter

from ..models import models
from ..services.db import listing_manager


router = APIRouter(
    prefix='/listings',
    tags=['listings']
)


# Create new listing
@router.post("/")
def create_listing(listing: models.Listing):
    return listing_manager.create_listing(listing.username, listing.title,
                                          listing.description, listing.location)


# Update an existing listing
@router.put("/update/")
def update_listing(update: models.UpdateListing):
    return listing_manager.update_listing(update.listing_id, update.title,
                                          update.description)


# Delete an existing listing
@router.delete("/{listing_id}")
def delete_listing(listing_id: int):
    return listing_manager.delete_listing(listing_id)


# Get an existing listing
@router.post("/search/")
def get_listing(search: models.SearchListings):
    return listing_manager.get_listings(search.listing_id, search.username,
                                        search.title, search.description, search.distance)
