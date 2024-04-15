import datetime

class Listing:
    """Listing object.

    Contains information relevant to a listing.
    
    Attributes:
        identifier (int): Unique id associated with the listing post.
        username (str): User who created the post.
        date (datetime.datetime): Time the post was created.
        title (str): The title associated with the listing post.
        description (str): The description associated with the listing post.
    """
    
    def __init__(self, identifier: int, username: str, date: datetime.datetime, title: str, description: str):
        self.identifier = identifier

        self.username = username
        self.date = date

        self.title = title
        self.description = description   