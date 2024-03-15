import mysql.connector
import dotenv
import os


dotenv.load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


def create_db() -> None:
    """Creates the table given in the environment file.
    
    The function will access MySQL with the given username and password.
    """
    
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {MYSQL_DB}")
    db.close()


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
            # Database does not yet exist
            create_db()

            # Recreate connection
            db = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB
            )
        elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            # Bad username / password
            raise Exception('Bad username or password')

    # Return the good connection
    return db


def create_tables() -> None:
    """Creates the tables necessary for the database.
    
    The function will not do anything if the tables already exist and will exit without error.
    """
    conn = connect()
    cursor = conn.cursor()

    # User details table
    user_details_query = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT UNSIGNED AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255), NOT NULL,
        description TEXT,
        profile_picture LONGBLOB,
        interest1 VARCHAR(255),
        interest2 VARCHAR(255),
        interest3 VARCHAR(255),
        gender VARCHAR(255),
        PRIMARY KEY (user_id),
        UNIQUE (username),
        UNIQUE (email),
    )    
    '''

    # Authentication table
    authentication_query = '''
    CREATE TABLE IF NOT EXISTS authentication (
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (username),
        FOREIGN KEY (username) REFERENCES profile(username),
    )
    '''

    # Listings table
    listings_query = '''
    CREATE TABLE IF NOT EXISTS listing (
        listing_id INT UNSIGNED AUTO_INCREMENT,
        user_id INT UNSIGNED,
        date DATETIME,
        title VARCHAR(255),
        description TEXT,
        PRIMARY KEY (listing_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    )
    '''
    
    # Execute queries
    conn.execute(user_details_query)
    conn.execute(authentication_query)
    conn.execute(listings_query)

    conn.close()
