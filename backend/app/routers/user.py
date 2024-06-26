from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, Any

from .auth import get_current_user, oauth2_bearer
from ..models import models
from ..services.db import user_manager
from ..services.oauth import decode_access_token


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.put("/update/")
def update_user_details(update: models.UpdateUserDetails, token: Annotated[str, Depends(oauth2_bearer)]):
    """Update an existing profile."""
    # Validate the token
    if decode_access_token(token) != update.username:
        raise HTTPException(status_code=403, detail="Could not update user details: authorization error.")

    status = user_manager.update_user(update.username, update.email, update.first_name, update.last_name,
                                      update.new_username)

    if status:
        return {
            "message": f"Updated user details for user {update.username}.",
            "status": "success"
        }
    else:
        raise HTTPException(status_code=409, detail=f"Could not update details for user {update.username}.")


@router.get("/usernameget/{username}")
def get_user_details_from_username(username: str):
    """Get user details with a username."""
    user_details = user_manager.get_user(username, is_username=True)

    if user_details:
        return {
            "result": user_details,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find user.")


@router.get("/idget/{user_id}")
def get_user_details_from_user_id(user_id: str):
    """Get user details with a user id."""
    user_details = user_manager.get_user(user_id, is_username=False)

    if user_details:
        return {
            "result": user_details,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=404, detail="Failed to find user.")


@router.get("/")
async def get_signed_in_user(user: dict[str, Any] = Depends(get_current_user)):
    """Get the profile of the signed-in user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    return user
