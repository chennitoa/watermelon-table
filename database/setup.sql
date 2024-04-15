CREATE DATABASE IF NOT EXISTS rent_a_friend;
USE rent_a_friend;

-- Users table, stores user information
CREATE TABLE IF NOT EXISTS user_information (
    user_id INT UNSIGNED AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (username),
    UNIQUE (email)
);

-- Profiles table, stores profile information
CREATE TABLE IF NOT EXISTS profiles (
    user_id INT UNSIGNED,
    description TEXT,
    profile_picture LONGBLOB,
    interest1 VARCHAR(255),
    interest2 VARCHAR(255),
    interest3 VARCHAR(255),
    gender VARCHAR(255),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user_information(user_id)
);

-- Authentication table, stores authentication information
CREATE TABLE IF NOT EXISTS auth (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES users(username)
);

-- Listing table, stores listing information
CREATE TABLE IF NOT EXISTS listing (
    listing_id INT UNSIGNED AUTO_INCREMENT,
    user_id INT UNSIGNED,
    date DATETIME,
    title VARCHAR(255),
    description TEXT,
    PRIMARY KEY (listing_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);