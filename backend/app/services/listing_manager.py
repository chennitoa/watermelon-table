from fastapi import HTTPException

from datetime import datetime

from .db_connect import connect
from ..models.models import Listing, UpdateListing


# Create new listing
def create_listing(listing: Listing):
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
def update_listing(listing_id: int, update: UpdateListing):
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
