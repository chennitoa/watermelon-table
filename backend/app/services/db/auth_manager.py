from passlib.context import CryptContext
from .user_manager import get_user

from .db_connect import connect


def create_auth(username: str, password: str, bcrypt_context: CryptContext) -> bool:
    """Create an authentication entry in the auth table.

    This function should not be called except for debugging purposes.
    An authentication entry is already created in create_user() to ensure atomicity.

    Args:
        username (str): The username associated with the user.
        password (str): The password that is used for authentication.
        bcrypt_context (passlib.context.CryptContext): The hashing context
        used for hashing the password.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        hashed_password = bcrypt_context.hash(password)

        # Check if user exists
        user_details = get_user(username, is_username=True)
        if not user_details:
            return False

        query = '''
        INSERT INTO auth(username, password)
        VALUES (%s, %s)
        '''

        values = (
            username,
            hashed_password
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def get_auth(username: str) -> dict | None:
    """Gets the authentication entry for the given user.

    Args:
        username (str): The username associated with the user.

    Returns:
        The authentication entry as a dict if it exists, else None.
    """
    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM auth WHERE username = %s"

        cursor.execute(query, (username, ))
        authentication = cursor.fetchone()

        if not authentication:
            return None

    return authentication


def update_auth(username: str, password: str, bcrypt_context: CryptContext) -> bool:
    """Updates the authentication entry for the given user.

    This function should only be used to change the password of the user.
    Username changes will be cascaded when the username changes with update_user().

    Args:
        username (str): The username associated with the user.
        password (str): The password that is used for authentication.
        bcrypt_context (passlib.context.CryptContext): The hashing context
        used for hashing the password.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        hashed_password = bcrypt_context.hash(password)

        # Check if user exists
        user_details = get_user(username, is_username=True)
        if not user_details:
            return False

        query = '''
        UPDATE auth SET
        password = %s
        WHERE username = %s
        '''

        values = (
            hashed_password,
            username
        )

        cursor.execute(query, values)
        conn.commit()

    return True


def delete_auth(username: str) -> bool:
    """Deletes the authentication entry for the given user.

    This function should not be called except for debugging purposes.
    If an authentication entry must be deleted, use delete_user() instead.
    If an authentication entry should be disabled, mark the profile as so.

    Args:
        username (str): The username associated with the user.

    Returns:
        True if the function succeeds, else False.
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists
        user_details = get_user(username, is_username=True)
        if not user_details:
            return False

        query = '''
        DELETE FROM auth
        WHERE username = %s
        '''

        cursor.execute(query, (username, ))
        conn.commit()

    return True
