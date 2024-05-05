from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, profiles, user, listings, ratings

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
app.include_router(profiles.router)
app.include_router(user.router)
app.include_router(listings.router)
app.include_router(ratings.router)
