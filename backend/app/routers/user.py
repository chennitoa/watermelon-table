from fastapi import APIRouter, Depends, HTTPException

from typing import Any

from . import auth
from ..models import models
from ..services.db import user_manager


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.put("/update/")
def update_user_details(update: models.UpdateUserDetails):
    """Update an existing profile."""
    return user_manager.update_user(update.username, update.email, update.first_name, update.last_name,
                                    update.new_username)


@router.get("/{username}")
def get_user_details(username: str):
    """Get user details with a username."""
    return user_manager.get_user(username)    


@router.get("/")
async def get_current_user(user: dict[str, Any] = Depends(auth.get_current_user)):
    """Get the profile of the signed-in user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    return user