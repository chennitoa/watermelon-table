from fastapi import HTTPException

from datetime import datetime

from .db_connect import connect
from .user_manager import get_user
from ..gmaps import *

def create_listing(username: str, title: str, listing_description: str = None, location: str = None):
    """Create a listing for the given username with the given details.

    Args:
        username (str): The username associated with the user.
        title (str): The title of the listing.
        listing_description (str): An optional long text blob description.
        location (str): The address of the listing. None defaults to the submitter's current location.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists and get the user id
        user_details = get_user(username, is_username=True)
        if user_details['status'] != "success":
            return {
                "message": f"Failed to find user {username}",
                "status": "failure"
            }

        if location is None:
            lat, long = get_current_location()
        else:
            try:
                lat, long = gmaps_api.geocode(location)[0]['geometry']['location'].values()
            except:
                return {
                    "message:": f"Invalid location: {location}. Enter a valid address.",
                    "status": "failure"
                }

        query = '''
        INSERT INTO listings (user_id, date, title, listing_description, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''

        values = (
            user_details['result']['user_id'],
            datetime.now(),
            title,
            listing_description,
            lat,
            long
        )

        cursor.execute(query, values)
        conn.commit()

    return {
        "message": f"New listing created for user {username}.",
        "status": "success"
    }


def get_listings(listing_id: int = None, username: str = None,
                 title_keywords: str = None, description_keywords: str = None, distance: float = None):
    """Get a listing depending on some search criteria:

    If listing_id is not null, then exactly one listing that matches the listing id will be returned.
    If username is not null, all listings will match the username given.
    If title_keywords is not null, all listings will contain the string given in the title.
    If description_keywords is not null, all listings will contain the string given in the description.
    If distance is not null, all listings will be within the specified radius in miles.

    If everything is null, then this function will return every single listing.

    If more complex searching is desired, then the results given should be filtered again with scripts.

    Args:
        listing_id (int): Matches the listing id for the listing.
        username (str): Matches the user who posted the listing.
        title_keywords (str): Matches for the specified string in the title.
        description_keywords (str): Matches for the specified string in the description.
        distance (float): Matches for listings within the specified radius in miles.

    Returns:
        The status of the call in a dictionary with the results in key 
        "results" as a list of listings dictionaries.
    """
    # Connect to SQL database
    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        if listing_id is not None:
            query = "SELECT * FROM listings WHERE listing_id = %s"

            cursor.execute(query, (listing_id, ))
            listing = cursor.fetchone()

            return {
                "results": [listing],
                "status": "success"
            }
        else:
            # Do nothing, simply continue, avoid nesting
            pass

        # Prepare a basic query
        query = "SELECT * FROM listings"
        conditions = []
        values = []

        if username is not None:
            user_details = get_user(username, is_username=True)
            if user_details['status'] == "failure":
                return {
                    "results": [],
                    "status": "success"
                }
            else:
                values.append(user_details['result']['user_id'])
                conditions.append("user_id = %s")
        else:
            # Do nothing, simply continue, avoid nesting
            pass

        if title_keywords is not None:
            values.append(f"%{title_keywords}%")
            conditions.append("title LIKE %s")
        else:
            # Do nothing, simply continue, avoid nesting
            pass

        if description_keywords is not None:
            values.append(f"%{description_keywords}%")
            conditions.append("listing_description LIKE %s")
        else:
            # Do nothing, simply continue, avoid nesting
            pass

        if distance is not None:
            lat, long = get_current_location()
            boundaries = calculate_boundaries((lat, long), distance)

            conditions.append("(latitude BETWEEN %s AND %s)")
            conditions.append("(longitude BETWEEN %s AND %s)")

            for boundary_line in boundaries.values():
                values.append(f"{boundary_line}")
        else:
            pass

        # Join the conditions together
        if conditions:
            query += " WHERE "
            query += " AND ".join(conditions)

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        listings = cursor.fetchall()

    return {
        "results": listings,
        "status": "success"
    }


def update_listing(listing_id: int, title: str = None, listing_description: str = None):
    """Update an existing listing with a different title or description.

    Cannot update the user id or the date.

    Args:
        listing_id (int): The id associated with the listing.
        title (str): The title of the listing.
        listing_description (str): An optional long text blob description.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """
    
    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if listing exists
        listings = get_listings(listing_id=listing_id)
        if not listings['results']:
            return {
                "message": f"Failed to find listing {listing_id}",
                "status": "failure"
            }

        query = '''
        UPDATE listings
        SET title = COALESCE(%s, title),
        listing_description = COALESCE(%s, listing_description)
        WHERE listing_id = %s
        '''

        values = (
            title,
            listing_description,
            listing_id,
        )

        cursor.execute(query, values)
        conn.commit()

    return {
        "message": f"Listing {listing_id} has been updated.",
        "status": "success"
    }


def delete_listing(listing_id: int):
    """Deletes the given listing with matching listing_id.

    Args:
        listing_id (int): The listing to delete.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """
    with connect() as conn:
        cursor = conn.cursor()

        # Check if listing exists
        listings = get_listings(listing_id=listing_id)
        if not listings['results']:
            return {
                "message": f"Failed to find listing {listing_id}",
                "status": "failure"
            }

        query = '''
        DELETE FROM listing
        WHERE listing_id = %s
        '''

        cursor.execute(query, (listing_id, ))
        conn.commit()

    return {
        "message": f"Listing {listing_id} has been deleted.",
        "status": "success"
    }

