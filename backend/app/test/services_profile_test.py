import unittest
from ..services.db import profile_manager


class ProfileGetTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetExistingProfile(self):
        profile = profile_manager.get_profile("dogman")
        expected_profile = {
            "user_id": 1,
            "profile_description": "The dog man.",
            "profile_picture": "HAHAHAHA",
            "interest1": "Dogs.",
            "interest2": "Eat",
            "interest3": "Running.",
            "gender": "Male"
        }

        # del is called to ensure that the key exists
        self.assertDictEqual(profile, expected_profile)

    def testGetNonexistentProfile(self):
        listing = profile_manager.get_profile("nobody")

        self.assertIs(listing, None)


if __name__ == "__main__":
    unittest.main()
