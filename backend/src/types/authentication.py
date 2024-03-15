

class Authentication:
    """Authentication object.
    
    Contains useful information for authenticating a user.

    Attributes:
        username (str): The username associated with the user.
        password (str): The password associated with the user's login.
    """
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
