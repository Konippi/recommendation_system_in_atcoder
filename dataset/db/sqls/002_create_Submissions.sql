CREATE TABLE IF NOT EXISTS Submissions(
    submission_id INT AUTO_INCREMENT,
    user_name VARCHAR(32) NOT NULL UNIQUE,
    date DATE NOT NULL,
    problem_name VARCHAR(32) NOT NULL UNIQUE,
    language VARCHAR(16) NOT NULL,
    status VARCHAR(4) NOT NULL,
    code_len VARCHAR(16) NOT NULL,
    runtime VARCHAR(16) NOT NULL,
    memory_usage VARCHAR(16) NOT NULL,
    PRIMARY KEY(submission_id),
    FOREIGN KEY fk_user_name(user_name) REFERENCES Users(user_name) ON DELETE CASCADE ON UPDATE CASCADE
);