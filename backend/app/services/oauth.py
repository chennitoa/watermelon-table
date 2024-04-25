from jose import jwt
from passlib.context import CryptContext

from datetime import datetime

from .db.auth_manager import get_auth


def authenticate(username: str, password: str, bcrypt_context: CryptContext) -> bool:
    """Authenticates the user by checking if the username and password are correct.

    Args:
        username (str): The username to identify.
        password (str): The password to authenticate.
    
    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """
    authentication = get_auth(username)

    if authentication['status'] != "success":
        return False  # Some kind of error happened trying to fetch the authentication
    elif not bcrypt_context.verify(password, authentication['result']['password']):
        return False  # The password is incorrect
    else:
        return authentication['result']


def create_access_token(username: str, secret: str, algo: str) -> str:
    """Creates a token to log in.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        The access token.
    """
    return jwt.encode({'sub': username, 'iat': datetime.now()},
                      secret, algorithm=algo)
