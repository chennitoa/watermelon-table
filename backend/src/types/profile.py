

class Profile:
    """Profile object

    Contains information for the profile.

    Attributes:
        first_name (str): First name of the profile.
        last_name (str): Last name of the profile.
        description (str): Description associated with the profile.
        profile_picture (str): Byte data associated with the image.
        interests (list[str]): A list of interests associated with the profile.
    """

    def __init__(self, first_name: str, last_name: str, description: str, profile_picture: str,
                 interests: list[str]):
        self.first_name = first_name
        self.last_name = last_name

        self.description = description
        self.profile_picture = profile_picture

        self.interests = interests
