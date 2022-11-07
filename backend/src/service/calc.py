import sys
sys.path.append('../../')
from backend.src.metadata.data import Data
import numpy as np
import csv
import statistics


def normalization(vec: list):
    vec = np.array(vec)
    vec_length = np.linalg.norm(vec)
    return vec / vec_length


class Recommend(Data):
    def __init__(self):
        self.ave_submission_num = None
        self.user_list = []
        self.submission_list = []
        self.problem_list = []
        self.problem_dict = {}
        self.problem_score_dict = {}
        self.user_based_table = []
        self.cos_similarity_dict = {}
        self.cos_similarity_tuple = ()
        self.target_user_list = []
        self.recommended_problem_list = []
        self.recommended_problem_with_user_dict = {}

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

        for problem in self.problem_list:
            self.problem_dict[(problem[0], problem[1])] = problem[2]
            self.problem_score_dict[(problem[0], problem[1])] = -1

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

    def set_learner_data(self, submission_info: list):
        Data.learner_vec.clear()
        latest_ac_date = ''
        for data in submission_info:
            contest = data['contest']
            submission_list = data['submissions']
            for submission_dict in reversed(submission_list):
                submission_date = submission_dict['date']
                problem = submission_dict['problem'].split(' ')[0]
                result = submission_dict['result']
                self.problem_score_dict[(contest, problem)] = 0
                if result == 'AC':
                    self.problem_score_dict[(contest, problem)] = 1
                    if latest_ac_date < submission_date:
                        Data.target_problem = (contest, problem)
                        latest_ac_date = submission_date

        for problem, score in self.problem_score_dict.items():
            Data.learner_vec.append(score)

    def set_target_users(self):
        for filter_user in self.filter_user_list:
            has_data = False
            for submissions in self.submission_by_user_dict[filter_user]:
                if submissions[1] == Data.target_problem[0] and submissions[2] == Data.target_problem[1]:
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
            learner_vec = normalization(Data.learner_vec)
            self.cos_similarity_dict[np.dot(normalized_ac_vec, learner_vec)] = self.target_user_list[i]

        # self.cos_similarity_tuple: (cos_similarity, user_name)
        self.cos_similarity_tuple = sorted(self.cos_similarity_dict.items(), reverse=True)

    def recommend_problem(self):
        for cos_similarity in self.cos_similarity_tuple:
            submissions = self.submission_by_user_dict[cos_similarity[1]]
            data_idx = 0
            for idx in range(len(submissions)):
                # conditions
                if submissions[idx][1] == Data.target_problem[0] and submissions[idx][2] == Data.target_problem[1] \
                        and submissions[idx][4] == 'AC' and idx + 1 < len(submissions):
                    data_idx = idx
                    break
            for nxt in range(data_idx+1, len(submissions)):
                filter_diff = chr(ord(Data.target_problem[1])+2) if Data.target_problem[1] not in ['F', 'G', 'Ex'] else 'Ex'
                if Data.target_problem[1] <= submissions[nxt][2] <= filter_diff and len(submissions[nxt][2]) <= len(filter_diff)  \
                        and submissions[nxt][4] == 'AC' and (submissions[nxt][1], submissions[nxt][2]) != (Data.target_problem[0], Data.target_problem[1]):
                    submission_tuple = (submissions[nxt][1], submissions[nxt][2])
                    if submission_tuple not in self.recommended_problem_list:
                        self.recommended_problem_list.append(submission_tuple)
                        self.recommended_problem_with_user_dict[submission_tuple] = {
                            'name': cos_similarity[1],
                            'cos_similarity': cos_similarity[0]
                        }
                    break

        recommended_problem_dict_list = []
        for recommended_problem in list(self.recommended_problem_list[:3]):
            recommended_problem_dict_list.append({
                'contest': recommended_problem[0],
                'problem': {
                    'diff': recommended_problem[1],
                    'title': self.problem_dict[(recommended_problem[0], recommended_problem[1])]
                },
                'user': self.recommended_problem_with_user_dict[(recommended_problem[0],recommended_problem[1])]
            })
        Data.recommended_problem_dict_list = recommended_problem_dict_list

    # calculate feature vector
    def calc_data(self, submission_info: list):
        self.set_data()
        self.filter_user()
        self.calc_ave_submission_num()
        self.set_submission_data_by_user()
        self.set_learner_data(submission_info=submission_info)
        self.set_target_users()
        self.create_user_based_table()
        self.calc_cos_similarity()
        self.recommend_problem()


class Calc:
    def __init__(self):
        self._recommend = Recommend()

    def calc(self, submission_info: list):
        self._recommend.calc_data(submission_info=submission_info)
