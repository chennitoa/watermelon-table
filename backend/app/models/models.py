from pydantic import BaseModel, Field

from datetime import datetime
from typing import Dict, Optional


class Profile(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    description: str
    profile_picture: str
    interest1: str
    interest2: str
    interest3: str
    gender: str


class UpdateProfile(BaseModel):
    username: Optional[str]
    email: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]
    interest1: Optional[str]
    interest2: Optional[str]
    interest3: Optional[str]


class Listing(BaseModel):
    user_id: int
    date: datetime
    title: str
    description: str


class UpdateListing(BaseModel):
    title: Optional[str]
    description: Optional[str]


class SearchListings(BaseModel):
    title: Optional[str]
    description: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class Auth(BaseModel):
    username: str
    password: str