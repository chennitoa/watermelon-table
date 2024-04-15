from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import Union

from .models import models
from .routers import auth
from .services import profile_manager, listing_manager

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

# Update an existing profile
@app.put("/profiles/{profile_id}")
def update_profile(profile_id: int, update: models.UpdateProfile):
    return profile_manager.update_profile(profile_id, update)

# Delete an existing profile
@app.delete('/profiles/{profile_id}')
def delete_profile(profile_id: int):
    return profile_manager.delete_profile(profile_id)

# Get an existing profile with user_id OR username
@app.get("/profiles/{identifier}")
def get_profile(identifier: Union[int, str]):
    return profile_manager.get_profile(identifier)    

# Get the profile of the signed-in user
@app.get("/profiles/")
async def get_current_profile(user: models.Profile = Depends(auth.get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed to authorize user.")
    return {"Profile": user}

# Create new listing
@app.post("/listings/")
def create_listing(listing: models.Listing):
    return listing_manager.create_listing(listing)

# Update an existing listing
@app.put("/listings/{listing_id}")
def update_listing(listing_id: int, update: models.UpdateListing):
    return listing_manager.update_listing(listing_id, update)

# Delete an existing listing
@app.delete('/listings/{listing_id}')
def delete_listing(listing_id: int):
    return listing_manager.delete_listing(listing_id)

# Get an existing listing
@app.get("/listings/{listing_id}")
def get_listing(listing_id: int):
    return listing_manager.get_listing(listing_id)
