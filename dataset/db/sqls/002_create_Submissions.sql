CREATE TABLE IF NOT EXISTS Submissions(
    submission_id INT AUTO_INCREMENT,
    user_name VARCHAR(32) NOT NULL,
    date VARCHAR(32) NOT NULL,
    contest_num VARCHAR(4) NOT NULL,
    problem_name VARCHAR(64) NOT NULL,
    language VARCHAR(64) NOT NULL,
    status VARCHAR(16) NOT NULL,
    code_len VARCHAR(16) NOT NULL,
    runtime VARCHAR(16) NOT NULL,
    memory_usage VARCHAR(16) NOT NULL,
    PRIMARY KEY(submission_id),
    FOREIGN KEY fk_user_name(user_name) REFERENCES Users(user_name) ON DELETE CASCADE ON UPDATE CASCADE
);