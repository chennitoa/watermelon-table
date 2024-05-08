from datetime import datetime

from .db_connect import connect
from .user_manager import get_user


def rate_profile(rater_name: str, rated_name: str, rating: int):
    """Rates an existing profile.

    Args:
        rater_name (str): The username of the rating user.
        rated_name (str): The username of the user receiving a rating.
        rating (int): The rating received by the receiving user. Ranges from 1 to 5.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if rater and rated exist
        rater = get_user(rater_name, is_username=True)
        rated = get_user(rated_name, is_username=True)

        if not rater or not rated:
            return False

        # Ensure users cannot rate themselves
        if rater_name == rated_name:
            return False

        exists = get_specific_rating(rater_name, rated_name)

        # If a rating already exists, update the rating.
        if exists:
            update_rating(rater_name, rated_name, rating)

            return True

        query = """
        INSERT INTO ratings (rater_name, rated_name, rating, rated_date)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            rater_name,
            rated_name,
            rating,
            datetime.now()
        )

        # Insert ratings into ratings table
        cursor.execute(query, values)
        conn.commit()

    return True


def update_rating(rater_name: str, rated_name: str, rating: int):
    """Updates the information of a user in the database.

    Args:
        rater_name (str): The username of the rating user.
        rated_name (str): The username of the user receiving a rating.
        rating (int): The rating received by the receiving user. Ranges from 1 to 5.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if users exist
        existing = get_specific_rating(rater_name, rated_name)

        if not existing:
            return False

        query = """
        UPDATE ratings SET
        rating = COALESCE(%s, rating),
        rated_date = %s
        WHERE rater_name = %s AND rated_name = %s
        """

        values = (
            rating,
            datetime.now(),
            rater_name,
            rated_name
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def get_ratings(username: str, is_rater: bool = False):
    """Searches for the ratings of a user in the database. If found, returns all ratings.

    Args:
        username (str): The username associated with the user.
        is_rater (bool): If true, returns all outgoing ratings from the user. Else, returns all ratings received.

    Returns:
        A list of all ratings received or given by the user.
    """

    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if user exists and get the user id
        user_details = get_user(username, is_username=True)

        if not user_details:
            return None

        if is_rater:
            query = "SELECT * FROM ratings WHERE rater_name = %s"
        else:
            query = "SELECT * FROM ratings WHERE rated_name = %s"

        cursor.execute(query, (user_details['username'], ))
        ratings = cursor.fetchall()

    return ratings


def get_specific_rating(rater_name: str, rated_name: str):
    """Searches for a specific rating in the database.

    Args:
        rater_name (str): The username of the rating user.
        rated_name (str): The username of the user receiving a rating.

    Returns:
        A dict with the details of the specific rating.
    """

    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if users exist
        userA_details = get_user(rater_name, is_username=True)
        userB_details = get_user(rated_name, is_username=True)

        if not userA_details or not userB_details:
            return None

        query = "SELECT * FROM ratings WHERE rater_name = %s AND rated_name = %s"

        cursor.execute(query, (rater_name, rated_name,))
        ratings = cursor.fetchone()

    return ratings


def get_user_rating(username: str):
    """Searches for the ratings of a user in the database and returns the average.

    Args:
        username (str): The username associated with the user.

    Returns:
        A dict containing the average rating for the user and the total number of ratings.
    """

    ratings = get_ratings(username, is_rater=False)

    if not ratings:
        # Return base rating of zero
        return {
            "rating": 0.0,
            "total_ratings": 0
        }

    # num = Sum of ratings
    # den = Total number of ratings
    num = 0
    den = 0

    for user in ratings:
        num += user['rating']
        den += 1

    avg_ratings = num / den

    return {
        "rating": avg_ratings,
        "total_ratings": den
    }
