import csv


class Data:
    userList = []
    submissionList = []


class Ac(Data):
    def __init__(self):
        self.userList = []
        self.submissionList = []

    def set_data(self):
        csv_file = open('../dataset/csv/data/user.csv', 'r')
        users = csv.reader(csv_file)
        for user in users:
            self.userList.append(user)

        csv_file = open('../dataset/csv/data/submission.csv', 'r')
        submissions = csv.reader(csv_file)
        for submission in submissions:
            self.submissionList.append(submission)

        Data.userList = self.userList
        Data.submissionList = self.submissionList
