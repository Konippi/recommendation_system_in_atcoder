import csv
import statistics
from analysis.src.metadata.data import Data


class Ac(Data):
    def __init__(self):
        self.userList = []
        self.submissionList = []

    # set data from csv
    def set_data(self):
        csv_file = open('../dataset/data/csv/user.csv', 'r')
        users = csv.reader(csv_file)
        for user in users:
            self.userList.append(user[0])
            self.ratingDict[user[0]] = int(user[1])

        csv_file = open('../dataset/data/csv/submission.csv', 'r')
        submissions = csv.reader(csv_file)
        for submission in submissions:
            self.submissionList.append(submission)

        Data.userList = self.userList
        Data.submissionList = self.submissionList

    # filter users who have no submissions for ABC
    def filter_user(self):
        submission_num_dict = {}
        for user in self.userList:
            submission_num_dict[user] = 0

        for submission in self.submissionList:
            submission_num_dict[submission[0]] += 1

        for user, submission_num in submission_num_dict.items():
            if submission_num > 0:
                self.filter_userList.append(user)

        for filter_user in self.filter_userList:
            self.submission_numDict[filter_user] = submission_num_dict[filter_user]

    def calc_ave_submission_num(self):
        submission_num_list = [submission_num for submission_num in self.submission_numDict.values()]
        self.ave_submissionNum = statistics.mean(submission_num_list)

    def set_submission_data_by_user(self):
        for filter_user in self.filter_userList:
            self.submission_by_userDict[filter_user] = []

        for submission in self.submissionList:
            submission_data = [
                submission[1],
                submission[2],
                submission[3],
                submission[5]
            ]
            self.submission_by_userDict[submission[0]].append(submission_data)

        # sort by date
        for filter_user in self.filter_userList:
            self.submission_by_userDict[filter_user] = sorted(self.submission_by_userDict[filter_user])

    def calc_patio_ac(self):
        pass

    # calculate feature vector
    def calc_feature_vec(self):
        self.set_data()
        self.filter_user()
        self.calc_ave_submission_num()
        self.set_submission_data_by_user()
        self.calc_patio_ac()


class Calc:
    def __init__(self):
        self._ac = Ac()

    def calc(self):
        self._ac.calc_feature_vec()
