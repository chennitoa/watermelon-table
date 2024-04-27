from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

import os
from typing import Annotated

from ..models import models
from ..services import oauth
from ..services.db import profile_manager, user_manager


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login/")


@router.post("/sign-up/")
async def signup(user: models.SignupDetails):
    """Create a user."""
    user_manager.create_user(user.username, user.email, user.first_name, user.last_name,
                             user.password, bcrypt_context)
    profile_manager.create_profile(user.username)  # Create a default empty profile

    return {"status": "success"}


@router.post("/login/", response_model=models.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Log in with username and password."""
    user = oauth.authenticate(form_data.username, form_data.password, bcrypt_context)
    if not user:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    token = oauth.create_access_token(user['username'], SECRET_KEY, ALGORITHM)

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Get the current signed-in user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise HTTPException(status_code=401, detail="Failed to authorize user.")
        return user_manager.get_user(username, is_username=True)
    except:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
