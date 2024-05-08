from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated

from .auth import oauth2_bearer
from ..models import models
from ..services.db import rating_manager, listing_manager
from ..services.oauth import decode_access_token


router = APIRouter(
    prefix='/ratings',
    tags=['ratings']
)


@router.post("/rate/")
def rate_profile(rating: models.Rating, token: Annotated[str, Depends(oauth2_bearer)]):
    """Submits a rating for a profile."""
    # Validate the token
    if decode_access_token(token) != rating.rater_name:
        raise HTTPException(status_code=403, detail="Could not create rating: authorization error.")

    # Validate the ratings
    if not 1 <= rating.rating <= 5:
        raise HTTPException(status_code=400, detail="Invalid rating. Rating must be between 1-5.")

    # Validate the username
    if rating.rater_name == rating.rated_name:
        raise HTTPException(status_code=400, detail="Cannot rate self.")

    status = rating_manager.rate_profile(rating.rater_name, rating.rated_name, rating.rating)

    if status:
        status = listing_manager.update_listing_ratings(rating.rated_name)

    if status:
        return {
            "message": f"User {rating.rater_name} rated {rating.rated_name}",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Failed to create rating for user {rating.rated_name}.")


@router.put("/update/")
def update_rating(update: models.Rating, token: Annotated[str, Depends(oauth2_bearer)]):
    """Update an existing rating."""
    # Validate the token
    if decode_access_token(token) != update.rater_name:
        raise HTTPException(status_code=403, detail="Could not update rating: authorization error.")

    status = rating_manager.update_rating(update.rater_name, update.rated_name, update.rating)

    if status:
        status = listing_manager.update_listing_ratings(update.rated_name)

    # If both functions succeed
    if status:
        return {
            "message": f"Rating for user {update.rated_name} has been updated.",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Failed to update rating for user {update.rated_name}")


@router.get("/all/{username}")
def get_rating(username: str):
    """Get all existing ratings for a user."""
    ratings = rating_manager.get_ratings(username)

    if ratings:
        return {
            "result": ratings,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find user.")


@router.post("/get/")
def get_specific_rating(rater_name: str, rated_name: str):
    """Get all existing ratings for a user."""
    ratings = rating_manager.get_specific_rating(rater_name, rated_name)

    if ratings:
        return {
            "result": ratings,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find user.")


@router.get("/average/{username}")
def get_user_rating(username: str):
    """Get the average rating for a user."""
    rating = rating_manager.get_user_rating(username)

    if rating:
        return {
            "result": rating,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find user.")
