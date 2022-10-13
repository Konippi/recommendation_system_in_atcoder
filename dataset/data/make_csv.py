import csv
from dataset.src.service import db


class Csv:
    def __init__(self):
        self.user_list = []
        self.submission_list = []
        self.problem_list = []
        self.sql = db.Sql()

    def make_csv(self):
        self.user_list = self.sql.get_user_details()
        self.submission_list = self.sql.get_submission_details()
        self.problem_list = self.sql.get_problem_details()

        with open('../data/csv/user.csv', 'w', newline='', errors='ignore') as f_user:
            writer_user = csv.writer(f_user)
            writer_user.writerows(self.user_list)

        with open('../data/csv/submission.csv', 'w', newline='', errors='ignore') as f_submission:
            writer_submission = csv.writer(f_submission)
            writer_submission.writerows(self.submission_list)

        with open('../data/csv/problem.csv', 'w', newline='', errors='ignore') as f_problem:
            writer_problem = csv.writer(f_problem)
            writer_problem.writerows(self.problem_list)

        print('complete!')
