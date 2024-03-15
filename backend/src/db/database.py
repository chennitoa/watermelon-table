import mysql.connector
import dotenv
import os


dotenv.load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


def create_db() -> None:
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {MYSQL_DB}")
    db.close()


def connect() -> mysql.connector.MySQLConnection:
    """Connects to a MYSQL server 
    
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
