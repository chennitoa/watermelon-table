from fastapi import HTTPException

from datetime import datetime

from .db_connect import connect
from ..models.models import Profile, UpdateProfile


# Create a new account
def signup(user: Profile, bcrypt_context):
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
def update_profile(profile_id: int, update: UpdateProfile):
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
