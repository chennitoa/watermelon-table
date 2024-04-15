import mysql.connector
import dotenv
import os


MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


def connect() -> mysql.connector.MySQLConnection:
    """Connects to a MYSQL server and returns the connection object.

    Note that the connection should be closed by any caller. Failure to do this 
    may result in future connections not being able to be allocated.

    Returns:
        A connection to the MySQL server.
    """
    try:
        db = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            # DB does not exist
            raise Exception('Could not find database.')
        elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            # Bad username / password
            raise Exception('Bad username or password.')

    # Return the good connection
    return db
