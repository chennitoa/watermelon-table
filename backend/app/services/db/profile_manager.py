from .db_connect import connect
from .user_manager import get_user


def create_profile(username: str, profile_description: str = None, profile_picture: str = None,
                   interest1: str = None, interest2: str = None, interest3: str = None,
                   gender: str = None) -> bool:
    """Creates a profile with the given value.

    Assumes that a user is created first. A user should be inserted into
    the user information table in the same function this is called in.

    Args:
        username (str): The username associated with the user.
        profile_description (str): An optional long text blob description.
        profile_picture (str): A byte string of data for the profile picture.
        interest1 (str): The first interest for the profile.
        interest2 (str): The second interest for the profile.
        interest3 (str): The third interest for the profile.
        gender (str): The entered gender for the profile.

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
        INSERT INTO profiles(user_id, profile_description, profile_picture, interest1, interest2, interest3, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        values = (
            user_details['user_id'],  # Get user id from user details query
            profile_description,
            profile_picture,
            interest1,
            interest2,
            interest3,
            gender
        )

        # Update profile in users table
        cursor.execute(query, values)
        conn.commit()

    return True


def get_profile(username: str) -> dict | None:
    """Searches for the profile of a user in the database. If found, returns all profile data.

    Args:
        username (str): The username associated with the user.

    Returns:
        The profile details as a dict if it exists, else None.
    """

    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if user exists and get the user id
        user_details = get_user(username, is_username=True)
        if not user_details:
            return None

        query = "SELECT * FROM profiles WHERE user_id = %s"

        cursor.execute(query, (user_details['user_id'], ))
        profile = cursor.fetchone()

    return profile


def update_profile(username: str, profile_description: str = None, profile_picture: str = None,
                   interest1: str = None, interest2: str = None, interest3: str = None,
                   gender: str = None):
    """Updates an existing profile with values.

    Args:
        username (str): The username associated with the user.
        profile_description (str): An optional long text blob description.
        profile_picture (str): A byte string of data for the profile picture.
        interest1 (str): The first interest for the profile.
        interest2 (str): The second interest for the profile.
        interest3 (str): The third interest for the profile.
        gender (str): The entered gender for the profile.

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
        UPDATE profiles
        SET profile_description = COALESCE(%s, profile_description),
        profile_picture = COALESCE(%s, profile_picture),
        interest1 = COALESCE(%s, interest1),
        interest2 = COALESCE(%s, interest2),
        interest3 = COALESCE(%s, interest3),
        gender = COALESCE(%s, gender)
        WHERE user_id = %s
        '''

        values = (
            profile_description,
            profile_picture,
            interest1,
            interest2,
            interest3,
            gender,
            user_details['user_id']
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def delete_profile(username: str):
    """Delete the profile associated to a user given their username.

    This function should not be called except for debugging purposes.
    If a profile must be deleted, use delete_user() instead.
    If a profile should be hidden, mark the profile as so.

    Args:
        username (str): The username associated with the user.

    Returns:
        True if the function succeeds, else False.
    """
    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists and get the user id
        user_details = get_user(username, is_username=True)
        if not user_details:
            return False

        # Set up query to delete users table
        query = '''
        DELETE FROM profiles
        WHERE user_id = %s
        '''

        # Delete profile in users table
        cursor.execute(query, (user_details['user_id'], ))
        conn.commit()

    return True
