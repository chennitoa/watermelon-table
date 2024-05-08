from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from typing import Annotated

from ..models import models
from ..services import oauth
from ..services.db import profile_manager, user_manager


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login/")


@router.post("/sign-up/")
async def signup(user: models.SignupDetails):
    """Create a user."""
    user_status = user_manager.create_user(user.username, user.email, user.first_name, user.last_name,
                                           user.password, bcrypt_context)
    profile_status = profile_manager.create_profile(user.username)  # Create a default empty profile

    if user_status:
        if profile_status:
            return {
                "message": f"Successfully created user {user.username}.",
                "status": "success"
            }
        else:
            return {
                "message": f"Successfully created user {user.username}. However, profile could not be created.",
                "status": "success"
            }
    else:
        raise HTTPException(status_code=409, detail="Failed to create user.")


@router.post("/login/", response_model=models.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Log in with username and password."""
    auth_success = oauth.authenticate(form_data.username, form_data.password, bcrypt_context)
    if not auth_success:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    token = oauth.create_access_token(form_data.username)

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Get the current signed-in user."""
    try:
        username = oauth.decode_access_token(token)
        if not username:
            raise HTTPException(status_code=401, detail="Failed to authorize user.")
        return user_manager.get_user(username, is_username=True)
    except Exception:
        # Any kind of error invalidates the login
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
