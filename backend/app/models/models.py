from pydantic import BaseModel

from typing import Optional


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
    username: str
    title: str
    description: Optional[str]
    location: Optional[str]


class UpdateListing(BaseModel):
    listing_id: int
    title: Optional[str]
    description: Optional[str]


class SearchListings(BaseModel):
    listing_id: Optional[int]
    username: Optional[str]
    title: Optional[str]
    description: Optional[str]
    distance: Optional[int]


class Token(BaseModel):
    access_token: str
    token_type: str


class Auth(BaseModel):
    username: str
    password: str