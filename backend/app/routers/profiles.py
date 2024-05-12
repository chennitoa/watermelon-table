from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated

from .auth import oauth2_bearer
from ..models import models
from ..services.db import profile_manager
from ..services.oauth import decode_access_token


router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.put("/update/")
def update_profile(update: models.UpdateProfile, token: Annotated[str, Depends(oauth2_bearer)]):
    """Update an existing profile."""
    # Validate the token
    if decode_access_token(token) != update.username:
        raise HTTPException(status_code=403, detail="Cannot update profile: authorization error.")

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
