import unittest
from ..services.db import listing_manager


class ListingGetTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetExistingListing(self):
        listing = listing_manager.get_listing(1)
        expected_listing = {
            "user_id": 1,
            "date": "1990-01-04 00:00:12",
            "title": "Looking for a dogsitter",
            "listing_description": "Dog sitting job. I pay $10.",
            "latitude": 37.3368,
            "longitude": -121.881,
            "street_address": "1 Washington Sq",
            "avg_user_rating": 0
        }

        # del is called to ensure that the key exists
        del listing["listing_id"]  # listing_id may be nondeterministic
        self.assertDictEqual(listing, expected_listing)

    def testGetNonexistentListing(self):
        listing = listing_manager.get_listing(99)

        self.assertIs(listing, None)


if __name__ == "__main__":
    unittest.main()
