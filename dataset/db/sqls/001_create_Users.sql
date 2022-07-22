CREATE TABLE IF NOT EXISTS Users(
    user_id INT AUTO_INCREMENT,
    user_name VARCHAR(32) NOT NULL UNIQUE,
    user_rating INT NOT NULL,
    PRIMARY KEY(user_id)
);