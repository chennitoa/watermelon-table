from passlib.context import CryptContext

from .db_connect import connect


def create_user(username: str, email: str, first_name: str, last_name: str,
                password: str, bcrypt_context: CryptContext):
    """Adds the specified user to the users database and adds the user's authentication details.

    The user's entry in the authentication table is also created here to ensure atomicity.

    Args:
        username (str): The username associated with the user.
        email (str): The email associated with the user.
        first_name (str): The first name associated with the user.
        last_name (str): The last name associated with the user.
        password (str): The password that is used for authentication.
        bcrypt_context (passlib.context.CryptContext): The hashing context
        used for hashing the password.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """

    with connect() as conn:
        cursor = conn.cursor()

        hashed_password = bcrypt_context.hash(password)

        user_query = '''
        INSERT INTO user_information (username, email, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        '''

        auth_query = '''
        INSERT INTO auth (username, password)
        VALUES (%s, %s)
        '''

        user_values = (
            username,
            email,
            first_name,
            last_name
        )

        auth_values = (
            username,
            hashed_password
        )

        # Insert new user into users table
        cursor.execute(user_query, user_values)
        # Insert authentication details into authentication table
        cursor.execute(auth_query, auth_values)
        conn.commit()

    return {
        "message": f"Successfully created user {username}.",
        "status": "success"
    }


def get_user(identifier: int | str):
    """Searches for a single user in the database. If found, returns all user details.

    If using this function, ensure that the user ID is only used internally.
    Do not send the user ID outside of the backend.

    Args:
        identifier (int | str): Either the internal user id of the user,
        if int, or the username of the user, if the value is a string

    Returns:
        The status of the call in a dictionary with the results in key 
        "result" as a user details dictionary.
    """

    with connect() as conn:
        cursor = conn.cursor(dictionary=True)

        # Check if input is a user ID or a username
        if identifier.isnumeric():
            query = "SELECT * FROM user_information WHERE user_id = %s"
        elif isinstance(identifier, str):
            query = "SELECT * FROM user_information WHERE username = %s"
        else:
            return {"status": "failure"}

        cursor.execute(query, (identifier, ))
        user_details = cursor.fetchone()

        if not user_details:
            return {"status": "failure"}

    return {
        "result": user_details,
        "status": "success"
    }


def update_user(username: str, email: str = None, first_name: str = None, last_name: str = None, new_username: str = None):
    """Updates the information of a user in the database.

    Args:
        username (str): The username associated with the user.
        email (str): The email associated with the user.
        first_name (str): The first name associated with the user.
        last_name (str): The last name associated with the user.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists
        user_details = get_user(username)
        if user_details['status'] == "failure":
            return {
                "message": f"Failed to find user {username}",
                "status": "failure"
            }

        query = '''
        UPDATE user_information SET
        username = COALESCE(%s, username),
        email = COALESCE(%s, email),
        first_name = COALESCE(%s, first_name),
        last_name = COALESCE(%s, last_name)
        WHERE username = %s
        '''

        values = (
            new_username,
            email,
            first_name,
            last_name,
            username
        )

        cursor.execute(query, values)
        conn.commit()

    return {
        "message": f"Updated user details for user {username}.",
        "status": "success" 
    }


def delete_user(username: str):
    """Completely delete a user and any information associated with the user from the database.

    Prefer to update user details with "deleted" rather than using this function.
    Protect this function with validation from the outside. This function does not 
    perform any internal validation.

    Args:
        username (str): The username associated with the user.

    Returns:
        A dict with two keys, "status" and "message". Status is the status
        of the user creation, either "success" or "failure".
    """

    with connect() as conn:
        cursor = conn.cursor()

        # Check if user exists
        user_details = get_user(username)
        if user_details['status'] == "failure":
            return {
                "message": f"Failed to find user {username}",
                "status": "failure"
            }

        query = '''
        DELETE FROM user_information
        WHERE username = %s 
        '''

        cursor.execute(query, (username, ))
        conn.commit()

    return {
        "message": f"Successfully deleted user {username}.",
        "status": "success"
    }
