#! /bin/sh

echo "-- Testing user service --"
python -m app.test.services_user_test

echo "-- Testing profile service --"
python -m app.test.services_profile_test

echo "-- Testing listing service --"
python -m app.test.services_listing_test