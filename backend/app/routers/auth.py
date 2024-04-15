from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

import dotenv
import os
from typing import Annotated

from ..models import models
from ..services import apifunc, oauth


dotenv.load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login/")


# Sign up / Create a profile
@router.post("/sign-up/")
async def signup(user: models.Profile):
    return apifunc.signup(user, bcrypt_context)


# Log in with username and password
@router.post("/login/", response_model=models.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = oauth.authenticate(form_data.username, form_data.password, bcrypt_context)
    if not user:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    token = oauth.create_access_token(user['username'], SECRET_KEY, ALGORITHM)

    return {'access_token': token, 'token_type': 'bearer'}


# Function to get the current signed-in user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise HTTPException(status_code=401, detail="Failed to authorize user.")
        return apifunc.get_profile(username)
    except:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
