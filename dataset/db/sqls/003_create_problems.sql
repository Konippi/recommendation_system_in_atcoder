CREATE TABLE IF NOT EXISTS problems(
    problem_id INT AUTO_INCREMENT,
    contest INT NOT NULL,
    difficulty VARCHAR(4) NOT NULL,
    title VARCHAR(64) NOT NULL,
    statement TEXT NOT NULL,
    PRIMARY KEY(problem_id)
);