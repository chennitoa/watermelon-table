from db.database import connect
from fastapi import HTTPException
from datetime import datetime
import api.models as models

# Create a new account
def signup(user: models.Profile, bcrypt_context):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor()

    # Parse profile
    user = user.model_dump()

    hashed_password = bcrypt_context.hash(user['password'])

    # Set up query to insert into users table
    query = '''
    INSERT INTO users (first_name, last_name, username, email, description, profile_picture, interest1, interest2, interest3, gender)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    # Query for authentication table
    queryAuth = '''
    INSERT INTO authentication (username, password)
    VALUES (%s, %s)
    '''

    # Set parameters for query
    values = (
        user['first_name'],
        user['last_name'],
        user['username'],
        user['email'],
        user['description'],
        user['profile_picture'],
        user['interest1'],
        user['interest2'],
        user['interest3'],
        user['gender']
    )

    valuesAuth = (
        user['username'],
        hashed_password
    )

    # Insert new profile into users table
    cursor.execute(query, values)
    # Insert authentication details into authentication table
    cursor.execute(queryAuth, valuesAuth)
    conn.commit()
    conn.close()

    return {"message": "New profile created."}

# Update an existing profile
def update_profile(profile_id: int, update: models.UpdateProfile):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # Parse updates to profile
    update = update.model_dump()

    # Get current profile
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (profile_id,))
    updated_profile = cursor.fetchone()

    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    # Update profile
    # If a field is empty, that field will not be updated/overwritten
    for key, value in update.items():
        if value != '':
            updated_profile[key] = value

    # Set up query to update users table
    query = '''
    UPDATE users
    SET first_name = %s, last_name = %s, username = %s, email = %s, description = %s, profile_picture = %s, interest1 = %s, interest2 = %s, interest3 = %s, gender = %s
    WHERE user_id = %s
    '''

    # Set parameters for query
    values = (
        updated_profile['first_name'],
        updated_profile['last_name'],
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

# Get an existing profile
def get_profile(identifier):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # Check if input is a user ID or a username
    if identifier.isnumeric():
        query = "SELECT * FROM users WHERE user_id = %s"
    elif isinstance(identifier, str):
        query = "SELECT * FROM users WHERE username = %s"
    else:
        raise HTTPException(status_code=400, detail="Invalid input. Must be a valid username or user ID.")

    cursor.execute(query, (identifier,))
    profile = cursor.fetchone()

    if not profile:
        raise HTTPException(status_code=404, detail="User does not exist.")

    conn.close()

    return profile

# Create new listing
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
def update_listing(listing_id: int, update: models.UpdateListing):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # Parse updates to listing
    update = update.model_dump()

    # Get current listing
    cursor.execute("SELECT * FROM listing WHERE listing_id = %s", (listing_id,))
    updated_listing = cursor.fetchone()

    if updated_listing is None:
        raise HTTPException(status_code=404, detail="Listing not found.")

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

# Get an existing listing
def get_listing(listing_id: int):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM listing WHERE listing_id = %s"

    cursor.execute(query, (listing_id,))
    listing = cursor.fetchone()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing does not exist.")

    conn.close()

    return listing

# Get all existing listings
def get_all_listings():
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    
    query = '''SELECT listing.*, users.username 
    FROM listing 
    JOIN users ON listing.user_id = users.user_id'''
    
    cursor.execute(query)
    listings = cursor.fetchall()
    
    if not listings:
        raise HTTPException(status_code=404, detail="No listings found.")
    
    conn.close()
    return listings
