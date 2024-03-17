from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Profile(BaseModel):
    first_name: str
    last_name: str
    email: str
    description: str
    profile_picture: str
    interests: List[str] = Field(..., max_items=3)

class UpdateProfile(BaseModel):
    username: Optional[str]
    email: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]
    interests: Optional[List[str]] = Field(..., max_items=3)

class Listing(BaseModel):
    user_id: int
    date: datetime
    title: str
    description: str

class UpdateListing(BaseModel):
    title: Optional[str]
    description: Optional[str]