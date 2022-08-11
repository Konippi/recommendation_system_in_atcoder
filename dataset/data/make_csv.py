import csv
from dataset.src.service import db


class Csv:
    def __init__(self):
        self.userList = []
        self.submissionList = []
        self.sql = db.Sql()

    def make_csv(self):
        self.userList = self.sql.get_user_details()
        self.submissionList = self.sql.get_submission_details()

        with open('../csv/data/user.csv', 'w', newline='', errors='ignore') as f_user:
            writer_user = csv.writer(f_user)
            writer_user.writerows(self.userList)

        with open('../csv/data/submission.csv', 'w', newline='', errors='ignore') as f_submission:
            writer_submission = csv.writer(f_submission)
            writer_submission.writerows(self.submissionList)

        print('complete!')
