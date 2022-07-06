CREATE TABLE IF NOT EXISTS Problems(
    problem_id INT AUTO_INCREMENT,
    user_name VARCHAR(32) NOT NULL UNIQUE,
    submission_date DATE NOT NULL,
    contest_name VARCHAR(32) NOT NULL UNIQUE,
    submission_result VARCHAR(32) NOT NULL,
    PRIMARY KEY(problem_id),
    FOREIGN KEY fk_user_name(user_name) REFERENCES Users(user_name) ON DELETE CASCADE ON UPDATE CASCADE
);