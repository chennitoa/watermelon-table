USE rent_a_lackey;

-- Users table, stores user information
CREATE TABLE IF NOT EXISTS user_information (
    user_id INT UNSIGNED AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (username),
    UNIQUE (email)
);

-- Profiles table, stores profile information
CREATE TABLE IF NOT EXISTS profiles (
    user_id INT UNSIGNED,
    profile_description TEXT,
    profile_picture LONGBLOB,
    interest1 VARCHAR(255),
    interest2 VARCHAR(255),
    interest3 VARCHAR(255),
    gender VARCHAR(255),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id)
        REFERENCES user_information(user_id)
        ON DELETE CASCADE
);

-- Authentication table, stores authentication information
CREATE TABLE IF NOT EXISTS auth (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username)
        REFERENCES user_information(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Listing table, stores listing information
CREATE TABLE IF NOT EXISTS listings (
    listing_id INT UNSIGNED AUTO_INCREMENT,
    user_id INT UNSIGNED,
    date DATETIME NOT NULL,
    title VARCHAR(255) NOT NULL,
    listing_description TEXT,
    latitude float,
    longitude float,
    street_address VARCHAR(255),
    avg_user_rating FLOAT,
    PRIMARY KEY (listing_id),
    FOREIGN KEY (user_id)
        REFERENCES user_information(user_id)
        ON DELETE CASCADE
);

-- Ratings table, stores ratings for profile
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT UNSIGNED AUTO_INCREMENT,
    rater_name VARCHAR(255) NOT NULL,
    rated_name VARCHAR(255) NOT NULL,
    rating INT NOT NULL,
    rated_date DATETIME NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (rated_name)
        REFERENCES user_information(username)
        ON DELETE CASCADE,
    FOREIGN KEY (rater_name)
        REFERENCES user_information(username)
        ON DELETE CASCADE,
    CONSTRAINT rating_range CHECK (rating>=1 AND rating<=5),
    UNIQUE KEY idx_unique_pairs (rater_name, rated_name)
);
