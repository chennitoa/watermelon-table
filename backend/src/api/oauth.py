import api.apifunc as apifunc
from datetime import datetime
from jose import jwt
from passlib.context import CryptContext
from db.database import connect
from fastapi import HTTPException

def get_auth(username: str):
    # Connect to SQL database
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM authentication WHERE username = %s"

    cursor.execute(query, (username,))
    auth = cursor.fetchone()

    if not auth:
        raise HTTPException(status_code=404, detail="User does not exist.")

    conn.close()

    return auth

# Authenticates the user by checking if the username and password are correct
def authenticate(username: str, password: str, bcrypt_context: CryptContext):
    user = get_auth(username)
    # Check if user exists in database
    if not user:
        return False
    # Check if password is correct
    if not bcrypt_context.verify(password, user['password']):
        return False
    return user

# Creates a token to log in
def create_access_token(username: str, secret: str, algo: str):
    return jwt.encode({'sub': username, 'iat': datetime.now()},
                      secret, algorithm=algo)
