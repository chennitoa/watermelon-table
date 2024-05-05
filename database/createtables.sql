USE rent_a_lackey;

INSERT INTO user_information (username, email, first_name, last_name)
    VALUES
    ("dogman", "dog@gmail.com", "Richard", "Dog"),
    ("frogman", "frog@gmail.com", "Fichard", "Frog"),
    ("clogman", "clog@gmail.com", "Chard", "Clog");

INSERT INTO auth (username, password)
    VALUES
    ("dogman", "182jec120e"),
    ("frogman", "39e0d9c"),
    ("clogman", "9120ek2");

INSERT INTO profiles(user_id, profile_description, profile_picture, interest1, interest2, interest3, gender)
    VALUES
    (1, "The dog man.", "HAHAHAHA", "Dogs.", "Eat", "Running.", "Male"),
    (2, "The frog man.", "LLLLLLLLL", "Frogs.", "Doing chores.", "Fishing.", "Female"),
    (3, "The clog man.", "PPPPPPPPP", "Clogs.", "Dogs.", "Walking.", "Female");

INSERT INTO listings (user_id, date, title, listing_description, latitude, longitude, street_address)
    VALUES
    (1, "1990-01-04 00:00:12", "Looking for a dogsitter", "Dog sitting job. I pay $10.", 37.3368, -121.881, "1 Washington Sq"),
    (2, "1995-02-05 00:00:23", "Looking for a frogsitter", "Frog sitting job. I pay $20.", 42.2616, -71.7957, "2 Washington Sq"),
    (3, "2024-03-21 00:12:55", "Looking for a clogsitter", "Clog sitting job. I pay $15.", 37.4223, -122.084, "1600 Amphitheatre Parkway");

INSERT INTO ratings (rater_name, rated_name, rating, rated_date)
    VALUES
    ("dogman", "frogman", "1", "2024-03-21 00:12:55"),
    ("dogman", "clogman", "5", "2024-03-25 20:20:55"),
    ("clogman", "frogman", "2", "2024-03-30 23:59:59");
