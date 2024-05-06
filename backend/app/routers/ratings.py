from typing import Any
from fastapi import APIRouter, HTTPException, Depends

from ..models import models
from ..services.db import rating_manager
from .auth import get_current_user
from ..services.db.listing_manager import update_listing_ratings


router = APIRouter(
    prefix='/ratings',
    tags=['ratings']
)


@router.post("/rate/")
def rate_profile(rating: models.Rating, current_user: dict[str, Any] = Depends(get_current_user)):
    '''Submits a rating for a profile'''
    if current_user['username'] != rating.rater_name:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")

    if not 1 <= rating.rating <= 5:
        raise HTTPException(status_code=400, detail="Invalid rating. Rating must be between 1-5.")

    status = rating_manager.rate_profile(rating.rater_name, rating.rated_name, rating.rating)

    update_listing_ratings(rating.rated_name)

    if status:
        return {
            "message": f"User {rating.rater_name} has successfully rated User {rating.rated_name} a {rating.rating} out of 5.",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Failed to create rating for user {rating.rated_name}.")


@router.put("/update/")
def update_rating(update: models.Rating):
    """Update an existing rating."""
    status = rating_manager.update_rating(update.rater_name, update.rated_name, update.rating)

    update_listing_ratings(update.rated_name)

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
