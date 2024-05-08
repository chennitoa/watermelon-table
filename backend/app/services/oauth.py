from jose import jwt
from passlib.context import CryptContext

from datetime import datetime
import os

from .db.auth_manager import get_auth


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def authenticate(username: str, password: str, bcrypt_context: CryptContext) -> bool:
    """Authenticates the user by checking if the username and password are correct.

    Args:
        username (str): The username to identify.
        password (str): The password to authenticate.

    Returns:
        True if authentication is a success, else False
    """
    authentication = get_auth(username)

    if not authentication:
        return False  # Some kind of error happened trying to fetch the authentication
    elif bcrypt_context.verify(password, authentication['password']):
        return True  # The password is correct
    else:
        return False  # Some other case, False by default


def create_access_token(username: str) -> str:
    """Creates a token to log in.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        The access token.
    """
    return jwt.encode({'sub': username, 'iat': datetime.now()},
                      SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(access_token: str) -> str | None:
    """Gets the username of the access token.

    Args:
        access_token (str): The access token to extract the username from.

    Returns:
        The username if the function is successful, else None
    """
    try:
        # Decode the token to get the result
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            # Something with the decoding process failed
            return None
        else:
            return username
    except Exception:
        # Invalid token, etc.
        return None
