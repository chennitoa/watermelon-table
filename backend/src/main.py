from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.database import connect
from api import models
from datetime import datetime

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

# Create a new profile
@app.post("/profiles/")
def create_profile(profile: models.Profile):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Parse profile
    profile = profile.model_dump()

    # Set up query to insert into users table
    query = '''
    INSERT INTO users (username, email, description, profile_picture, interest1, interest2, interest3, gender)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    interests = profile['interests']
    while len(interests) < 3:
        interests.append('')

    # Set parameters for query
    values = (
        profile['first_name'] + " " + profile['last_name'],
        profile['email'],
        profile['description'],
        profile['profile_picture'],
        interests[0],
        interests[1],
        interests[2],
        '',
    )

    # Insert new profile into users table
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": "New profile created."}

# Update an existing profile
@app.put("/profiles/{profile_id}")
def update_profile(profile_id: int, update: models.UpdateProfile):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Parse updates to profile
    update = update.model_dump()

    # Get current profile
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (profile_id,))
    current_profile = cursor.fetchone()

    if current_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    # Assign column names to current profile
    updated_profile = dict(zip(cursor.column_names, current_profile))

    # Update profile
    # If a field is empty, that field will not be updated/overwritten
    for key, value in update.items():
        # Case for list of interests
        if isinstance(value, list):
            for i in range(len(value)):
                if i == 0 and value != '':
                    updated_profile['interest1'] = value[i]
                elif i == 1 and value != '':
                    updated_profile['interest2'] = value[i]
                elif i == 2 and value != '':
                    updated_profile['interest3'] = value[i]
        # Case for all other parameters
        elif value != '':
            updated_profile[key] = value

    # Set up query to update users table
    query = '''
    UPDATE users
    SET username = %s, email = %s, description = %s, profile_picture = %s, interest1 = %s, interest2 = %s, interest3 = %s, gender = %s
    WHERE user_id = %s
    '''

    # Set parameters for query
    values = (
        updated_profile['username'],
        updated_profile['email'],
        updated_profile['description'],
        updated_profile['profile_picture'],
        updated_profile['interest1'],
        updated_profile['interest2'],
        updated_profile['interest3'],
        updated_profile['gender'],
        profile_id,
    )

    # Update profile in users table
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": f"Profile {profile_id} has been updated."}

# Delete an existing profile
@app.delete('/profiles/{profile_id}')
def delete_profile(profile_id: int):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Get current profile
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (profile_id,))
    current_profile = cursor.fetchone()

    if current_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    # Set up query to delete users table
    query = '''
    DELETE FROM users
    WHERE user_id = %s
    '''

    # Delete profile in users table
    cursor.execute(query, (profile_id,))
    conn.commit()
    conn.close()

    return {"message": f"Profile {profile_id} has been deleted."}

# Create new listing
@app.post("/listings/")
def create_listing(listing: models.Listing):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Parse listing
    listing = listing.model_dump()

    # Check if user creating the listing exists
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (listing['user_id'],))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    
    # Set up query to insert into listing table
    query = '''
    INSERT INTO listing (user_id, date, title, description)
    VALUES (%s, %s, %s, %s)
    '''

    # Set parameters for query
    values = (
        listing['user_id'],
        datetime.now(),
        listing['title'],
        listing['description'],
    )

    # Insert new listing into listing table
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": "New listing created."}

# Update an existing listing
# User id and date can not be updated
@app.put("/listings/{listing_id}")
def update_listing(listing_id: int, update: models.UpdateListing):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Parse updates to listing
    update = update.model_dump()

    # Get current listing
    cursor.execute("SELECT * FROM listing WHERE listing_id = %s", (listing_id,))
    current_listing = cursor.fetchone()

    if current_listing is None:
        raise HTTPException(status_code=404, detail="Listing not found.")

    # Assign column names to current profile
    updated_listing = dict(zip(cursor.column_names, current_listing))

    # Update listing
    # If a field is empty, that field will not be updated/overwritten
    for key, value in update.items():
        if value != '':
            updated_listing[key] = value

    # Set up query to update listing table
    query = '''
    UPDATE listing
    SET title = %s, description = %s
    WHERE listing_id = %s
    '''

    # Set parameters for query
    values = (
        updated_listing['title'],
        updated_listing['description'],
        listing_id,
    )

    # Update listing in users table
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": f"Listing {listing_id} has been updated."}

# Delete an existing listing
@app.delete('/listings/{listing_id}')
def delete_listing(listing_id: int):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Get current listing
    cursor.execute("SELECT * FROM listing WHERE listing_id = %s", (listing_id,))
    current_listing = cursor.fetchone()

    if current_listing is None:
        raise HTTPException(status_code=404, detail="Listing not found.")

    # Set up query to delete listing table
    query = '''
    DELETE FROM listing
    WHERE listing_id = %s
    '''

    # Delete listing in listing table
    cursor.execute(query, (listing_id,))
    conn.commit()
    conn.close()

    return {"message": f"Listing {listing_id} has been deleted."}