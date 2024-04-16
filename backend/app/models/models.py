from pydantic import BaseModel, Field

from datetime import datetime
from typing import Dict, Optional


class SignupDetails(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class UserDetails(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UpdateUserDetails(BaseModel):
    username: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    new_username: Optional[str]


class Profile(BaseModel):
    username: str
    description: Optional[str]
    profile_picture: Optional[str]
    interest1: Optional[str]
    interest2: Optional[str]
    interest3: Optional[str]
    gender: Optional[str]


class UpdateProfile(BaseModel):
    username: str
    description: Optional[str]
    profile_picture: Optional[str]
    interest1: Optional[str]
    interest2: Optional[str]
    interest3: Optional[str]
    gender: Optional[str]


class Listing(BaseModel):
    user_id: int
    date: datetime
    title: str
    description: Optional[str]


class UpdateListing(BaseModel):
    listing_id: int
    title: Optional[str]
    description: Optional[str]


class SearchListings(BaseModel):
    listing_id: Optional[int]
    username: Optional[int]
    title: Optional[str]
    description: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class Auth(BaseModel):
    username: str
    password: str