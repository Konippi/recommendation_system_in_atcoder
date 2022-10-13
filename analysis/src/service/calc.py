import numpy as np
import csv
import statistics
from analysis.src.metadata.data import Data


def normalization(vec):
    vec = np.array(vec)
    vec_length = np.linalg.norm(vec)
    return vec / vec_length


class Ac(Data):
    def __init__(self):
        self.user_list = []
        self.submission_list = []
        self.problem_list = []
        self.user_based_table = []
        self.cos_similarity_dict = {}
        self.cos_similarity_tuple = ()
        self.recommend_problem_set = set()
        self.target_user_list = []

        # test data
        self.test_vec = []
        self.test_problem = ['200', 'B']

    # set data from csv
    def set_data(self):
        csv_file = open('../dataset/data/csv/user.csv', 'r')
        users = csv.reader(csv_file)
        for user in users:
            self.user_list.append(user[0])
            self.rating_dict[user[0]] = int(user[1])

        csv_file = open('../dataset/data/csv/submission.csv', 'r')
        submissions = csv.reader(csv_file)
        for submission in submissions:
            self.submission_list.append(submission)

        csv_file = open('../dataset/data/csv/problem.csv', 'r')
        problems = csv.reader(csv_file)
        for problem in problems:
            self.problem_list.append(problem)

        Data.userList = self.user_list
        Data.submissionList = self.submission_list
        Data.problem_list = self.problem_list

    # filter user who has no submissions for ABC
    def filter_user(self):
        submission_num_dict = {}
        for user in self.user_list:
            submission_num_dict[user] = 0

        for submission in self.submission_list:
            submission_num_dict[submission[0]] += 1

        for user, submission_num in submission_num_dict.items():
            if submission_num > 0:
                self.filter_user_list.append(user)

        for filter_user in self.filter_user_list:
            self.submission_num_dict[filter_user] = submission_num_dict[filter_user]

    def calc_ave_submission_num(self):
        submission_num_list = [submission_num for submission_num in self.submission_num_dict.values()]
        self.ave_submission_num = statistics.mean(submission_num_list)

    def set_submission_data_by_user(self):
        for filter_user in self.filter_user_list:
            self.submission_by_user_dict[filter_user] = []

        for submission in self.submission_list:
            submission_data = [
                submission[1],
                submission[2],
                submission[3],
                submission[4],
                submission[6]
            ]
            self.submission_by_user_dict[submission[0]].append(submission_data)

        # sort by date
        for filter_user in self.filter_user_list:
            self.submission_by_user_dict[filter_user] = sorted(self.submission_by_user_dict[filter_user])

    def set_test_data(self):
        for problem in self.problem_list:
            if problem[0] == self.test_problem[0] and problem[1] == self.test_problem[1]:
                self.test_vec.append(1)
            else:
                self.test_vec.append(0)

    def set_target_users(self):
        for filter_user in self.filter_user_list:
            has_data = False
            for submissions in self.submission_by_user_dict[filter_user]:
                if submissions[1] == self.test_problem[0] and submissions[2] == self.test_problem[1]:
                    has_data = True
                    break
            if has_data:
                self.target_user_list.append(filter_user)

    def create_user_based_table(self):
        for target_user in self.target_user_list:
            ac_list_by_user = []
            for problem in Data.problem_list:
                is_ac = False
                has_data = False
                for submissions in self.submission_by_user_dict[target_user]:
                    if submissions[3] == problem[2]:
                        has_data = True
                        if submissions[4] == 'AC':
                            is_ac = True
                            break
                if is_ac:
                    ac_list_by_user.append(1)
                elif has_data:
                    ac_list_by_user.append(0)
                else:
                    ac_list_by_user.append(-1)
            self.user_based_table.append(ac_list_by_user)

    def calc_cos_similarity(self):
        # len(self.user_based_table) = len(self.target_user_list)
        for i in range(len(self.user_based_table)):
            normalized_ac_vec = normalization(self.user_based_table[i])
            test_vec = normalization(self.test_vec)
            self.cos_similarity_dict[np.dot(normalized_ac_vec, test_vec)] = self.target_user_list[i]

        # self.cos_similarity_tuple: (cos_similarity, user_name)
        self.cos_similarity_tuple = sorted(self.cos_similarity_dict.items(), reverse=True)
        self.cos_similarity_tuple = self.cos_similarity_tuple[:Data.collaborative_filtering_target_num]
        print(self.cos_similarity_tuple)

    def recommend_problem(self):
        for cos_similarity in self.cos_similarity_tuple:
            submissions = self.submission_by_user_dict[cos_similarity[1]]
            data_idx = 0
            for idx in range(len(submissions)):
                # conditions
                if submissions[idx][1] == self.test_problem[0] and submissions[idx][2] == self.test_problem[1] \
                        and submissions[idx][4] == 'AC' and idx + 1 < len(submissions):
                    data_idx = idx
                    break
            for nxt in range(data_idx+1, len(submissions)):
                if submissions[nxt][2] >= self.test_problem[1] and submissions[nxt][4] == 'AC':
                    self.recommend_problem_set.add((submissions[nxt][1], submissions[nxt][2]))
                    break
        self.recommend_problem_set.discard((self.test_problem[0], self.test_problem[1]))
        print(self.recommend_problem_set)

    # calculate feature vector
    def calc_data(self):
        self.set_data()
        self.filter_user()
        self.calc_ave_submission_num()
        self.set_submission_data_by_user()
        self.set_test_data()
        self.set_target_users()
        self.create_user_based_table()
        self.calc_cos_similarity()
        self.recommend_problem()


class Calc:
    def __init__(self):
        self._ac = Ac()

    def calc(self):
        self._ac.calc_data()
