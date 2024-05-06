import unittest
from ..services.db import user_manager


class AuthGetTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetExistingUser(self):
        user = user_manager.get_user("dogman")
        expected_user = {
            "username": "dogman",
            "email": "dog@gmail.com",
            "first_name": "Richard",
            "last_name": "Dog"
        }

        # del is called to ensure that the key exists
        del user["user_id"]  # user_id may be nondeterministic
        self.assertDictEqual(user, expected_user)

    def testGetNonexistentUser(self):
        user = user_manager.get_user("nobody")

        self.assertIs(user, None)


if __name__ == "__main__":
    unittest.main()
