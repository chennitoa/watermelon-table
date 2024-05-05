from fastapi import APIRouter, HTTPException

from ..models import models
from ..services.db import profile_manager


router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.put("/update/")
def update_profile(update: models.UpdateProfile):
    """Update an existing profile."""
    status = profile_manager.update_profile(update.username, update.description, update.profile_picture,
                                            update.interest1, update.interest2, update.interest3, update.gender)

    if status:
        return {
            "message": f"Profile for user {update.username} has been updated.",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Failed to update profile for user {update.username}")


@router.get("/{username}")
def get_profile(username):
    """Get an existing profile with a username."""
    profile = profile_manager.get_profile(username)

    if profile:
        return {
            "result": profile,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Failed to find user {username}")
