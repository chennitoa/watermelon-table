from datetime import datetime

from .db_connect import connect
from .user_manager import get_user


def create_listing(username: str, title: str, listing_description: str = None,
                   lat: float = None, long: float = None, location: str = None):
    """Create a listing for the given username with the given details.

    Args:
        username (str): The username associated with the user.
        title (str): The title of the listing.
        listing_description (str): An optional long text blob description.
        location (str): The address of the listing. None defaults to the submitter's current location.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists and get the user id
        user_details = get_user(username, is_username=True)
        if not user_details:
            return False

        query = '''
        INSERT INTO listings (user_id, date, title, listing_description, latitude, longitude, street_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        values = (
            user_details['user_id'],
            datetime.now(),
            title,
            listing_description,
            lat,
            long,
            location
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def get_listing(listing_id: int) -> dict | None:
    """Get a listing based on its unique listing id.

    Args:
        listing_id (int): Matches the listing id for the listing.

    Returns:
        The single listing as a dict if it exists, else None.
    """
    with connect() as conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM listings WHERE listing_id = %s"

        cursor.execute(query, (listing_id, ))
        listing = cursor.fetchone()

        if not listing:
            return None

    return listing


def search_listings(username: str = None, title_keywords: str = None,
                    description_keywords: str = None,
                    lat: float = None, long: float = None, distance: float = None) -> list[dict]:
    """Get a listing depending on some search criteria:

    If username is not null, all listings will match the username given.
    If title_keywords is not null, all listings will contain the string given in the title.
    If description_keywords is not null, all listings will contain the string given in the description.
    If distance is not null, all listings will be within the specified radius in miles.

    If everything is null, then this function will return every single listing.

    If more complex searching is desired, then the results given should be filtered again with scripts.

    Args:
        username (str): Matches the user who posted the listing.
        title_keywords (str): Matches for the specified string in the title.
        description_keywords (str): Matches for the specified string in the description.
        distance (float): Matches for listings within the specified radius in miles.

    Returns:
        The matched listings as a list of dicts.
    """
    # Connect to SQL database
    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Prepare a basic query
        query = "SELECT * FROM listings"
        conditions = []
        values = []

        if username is not None:
            user_details = get_user(username, is_username=True)
            if not user_details:
                return []
            else:
                values.append(user_details['user_id'])
                conditions.append("user_id = %s")

        if title_keywords is not None:
            values.append(f"%{title_keywords}%")
            conditions.append("title LIKE %s")

        if description_keywords is not None:
            values.append(f"%{description_keywords}%")
            conditions.append("listing_description LIKE %s")

        # Join the conditions together
        if conditions:
            query += " WHERE "
            query += " AND ".join(conditions)

        if lat is not None and long is not None and distance is not None:
            # Spherical Law of Cosines Formula
            # Parameters are in order: latitude, longitude, latitude, distance
            query += """
            HAVING
            (3959 * acos(cos(radians(%s)) * cos(radians(latitude))
            * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude))))
            < %s
            """
            values += [lat, long, lat, distance]

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        listings = cursor.fetchall()

    return listings


def update_listing(listing_id: int, title: str = None, listing_description: str = None,
                   lat: float = None, long: float = None, location: str = None):
    """Update an existing listing with a different title, description, or location.

    Cannot update the user id or the date.

    Args:
        listing_id (int): The id associated with the listing.
        title (str): The title of the listing.
        listing_description (str): An optional long text blob description.
        address (str): The street address of the listing.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if listing exists
        listing = get_listing(listing_id=listing_id)
        if not listing:
            return False

        query = '''
        UPDATE listings
        SET title = COALESCE(%s, title),
        listing_description = COALESCE(%s, listing_description),
        latitude = COALESCE(%s, latitude),
        longitude = COALESCE(%s, longitude),
        street_address = COALESCE(%s, street_address)
        WHERE listing_id = %s
        '''

        values = (
            title,
            listing_description,
            lat,
            long,
            location,
            listing_id,
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def delete_listing(listing_id: int) -> bool:
    """Deletes the given listing with matching listing_id.

    Args:
        listing_id (int): The listing to delete.

    Returns:
        True if the function succeeds, else False.
    """
    with connect() as conn:
        cursor = conn.cursor()

        # Check if listing exists
        listing = get_listing(listing_id=listing_id)  # Should only return one
        if not listing:
            return False

        query = '''
        DELETE FROM listings
        WHERE listing_id = %s
        '''

        cursor.execute(query, (listing_id, ))
        conn.commit()

    return True
