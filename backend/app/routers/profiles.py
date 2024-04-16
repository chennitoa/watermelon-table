from fastapi import APIRouter

from ..models import models
from ..services.db import profile_manager


router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.put("/update/")
def update_profile(update: models.UpdateProfile):
    """Update an existing profile."""
    return profile_manager.update_profile(update.username, update.description, update.profile_picture,
                                          update.interest1, update.interest2, update.interest3, update.gender)


@router.get("/{username}")
def get_profile(username):
    """Get an existing profile with a username."""
    return profile_manager.get_profile(username)    
