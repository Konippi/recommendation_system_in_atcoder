from dataset.metadata.data import Data
from dataset.src.service import db

import time
import requests
import re
from bs4 import BeautifulSoup


class Users(Data):
    def __init__(self):
        self._sql = db.Sql()
        self.ranking_url = 'https://atcoder.jp/ranking?page='
        self.page = 0
        self.user_num = 100
        self.user_list = []
        self.rating_list = []

    def collect_users(self):
        print('----------')
        print('Start collecting user\'s info')
        print('----------')

        # truncate user's data
        if input('Do you want to get the user\'s data? (y/n) > ') == 'y':
            self._sql.truncate('users')
        else:
            Data.user_list = self._sql.get_users_data(self.user_num)
            return

        # top 1000 user's data
        for page_num in range(self.user_num // 100):
            html = requests.get(self.ranking_url + str(page_num + 1), headers=Data.UA)
            soup = BeautifulSoup(html.content, 'html.parser')

            # userName
            for name in soup.find_all('a', class_=re.compile('username')):
                self.user_list.append(name.text)

            # rating
            judge_rating = 0
            for rating in soup.findAll('b'):
                if judge_rating % 2 == 0:
                    self.rating_list.append(int(rating.text))
                judge_rating += 1

            self.page += 1

            print(str(100 * self.page) + ' users: complete!')

        self._sql.set_users_data(self.user_num, self.user_list, self.rating_list)
        Data.user_list = self.user_list


class Submissions(Data):
    def __init__(self):
        self.data_num = 0
        self.user_name_list = []
        self.date_list = []
        self.contest_list = []
        self.problem_difficulty_list = []
        self.problem_title_list = []
        self.language_list = []
        self.status_list = []
        self.code_length_list = []
        self.runtime_list = []
        self.memory_usage_list = []
        self._sql = db.Sql()

    # clear
    def initialization(self):
        self.data_num = 0
        self.user_name_list.clear()
        self.date_list.clear()
        self.contest_list.clear()
        self.problem_difficulty_list.clear()
        self.problem_title_list.clear()
        self.language_list.clear()
        self.status_list.clear()
        self.code_length_list.clear()
        self.runtime_list.clear()
        self.memory_usage_list.clear()

    # each of contests
    def collect_submissions(self):
        print('\n----------')
        print('Start collecting submission\'s info')
        print('----------')

        # truncate submission's data
        if input('Do you want to get the submission\'s data? (y/n) > ') == 'y':
            self._sql.truncate('submissions')
        else:
            Data.next_contest = int(self._sql.get_now_contest()) + 1
            if Data.next_contest == Data.last_contest + 1:
                return

        # contest: now contest - last contest
        for contest in range(Data.next_contest, Data.last_contest + 1):
            print('\n----- ABC' + str(contest) + ' -----\n')

            # initialization
            self.initialization()

            # the existed contest
            if self._sql.is_existed(contest):
                print('already existed!')
                continue

            for user in Data.user_list:
                submission_url = 'https://atcoder.jp/contests/abc' + str(contest).zfill(3) + \
                                 '/submissions?f.User=' + user
                html = requests.get(submission_url, headers=Data.UA)
                soup = BeautifulSoup(html.content, 'html.parser')

                # table check
                table = soup.find('table')
                if table is None:
                    # 403: Forbidden
                    if html.status_code == 403:
                        print('!----Status Code: 403----!')
                        return 0

                    time.sleep(0.5)
                    continue

                data_list = soup.find('tbody').find_all('tr')

                for data in data_list:
                    # date
                    date = data.find('time', class_='fixtime-second').text
                    # remove timezone
                    self.date_list.append(date[:19])

                    # problem
                    problem = data.find(href=re.compile(r'/tasks/')).text
                    problem_data = problem.split(' - ')
                    problem_difficulty = problem_data[0]
                    problem_title = problem_data[1]
                    self.problem_difficulty_list.append(problem_difficulty)
                    self.problem_title_list.append(problem_title)

                    # user
                    self.user_name_list.append(user)

                    # language
                    language = data.find(href=re.compile(r'Language=')).text
                    self.language_list.append(language)

                    # status
                    status = data.find('span', class_=re.compile('label-')).text
                    self.status_list.append(status)

                    # codeLength, runtime, memoryUsage
                    detail_num = 0
                    for detail in data.find_all('td', class_='text-right'):
                        # codeLength
                        if detail_num == 1:
                            code_length = detail.text
                            self.code_length_list.append(code_length)

                            # CE process
                            if status == 'CE':
                                self.runtime_list.append(str(0) + 'ms')
                                self.memory_usage_list.append(str(0) + 'KB')

                        # runtime
                        if detail_num == 2:
                            runtime = detail.text
                            self.runtime_list.append(runtime)

                        # memoryUsage
                        if detail_num == 3:
                            memory_usage = detail.text
                            self.memory_usage_list.append(memory_usage)

                        detail_num += 1

                    # contest
                    self.contest_list.append(str(contest).zfill(3))

                    # data_num
                    self.data_num += 1

                time.sleep(0.5)

            self._sql.set_submissions_data(self.data_num, self.user_name_list, self.date_list,
                                           self.contest_list, self.problem_difficulty_list, self.problem_title_list,
                                           self.language_list, self.status_list, self.code_length_list,
                                           self.runtime_list, self.memory_usage_list)


class Problems(Data):
    def __init__(self):
        self._sql = db.Sql()
        self.contest_list = []
        self.difficulty_list = []
        self.title_list = []
        self.statement_list = []

    # all at once
    def collect_problems(self):
        print('\n----------')
        print('Start collecting problem\'s info')
        print('----------')

        # truncate problem's data
        if input('Do you want to get the problem\'s data? (y/n) > ') == 'y':
            self._sql.truncate('problems')
        else:
            return

        for contest in range(1, Data.last_contest + 1):
            problem_url = 'https://atcoder.jp/contests/abc' + str(contest).zfill(3) + '/tasks'
            html = requests.get(problem_url, headers=Data.UA)
            soup = BeautifulSoup(html.content, 'html.parser')

            data_list = []

            for data in soup.findAll(href=re.compile(r'/tasks/')):
                data_list.append(data.text)

            i = 0
            for data in data_list:
                if i % 2 == 0:
                    self.difficulty_list.append(data)
                else:
                    self.title_list.append(data)
                i += 1

            for problem_num in range(len(data_list) // 2):
                difficulty = chr(97 + problem_num)
                last_path = 'abc' + str(contest).zfill(3) + '_' + str(problem_num + 1)

                # preprocess
                if contest >= 20:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'abc' + str(contest).zfill(3) + '_' + difficulty
                if 42 <= contest <= 50:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 16).zfill(3) + '_' + difficulty
                if 52 <= contest <= 53:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 15).zfill(3) + '_' + difficulty
                if 55 <= contest <= 56:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 14).zfill(3) + '_' + difficulty
                if 58 <= contest <= 60:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 13).zfill(3) + '_' + difficulty
                if 62 <= contest <= 63:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 12).zfill(3) + '_' + difficulty
                if 65 <= contest <= 69:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 11).zfill(3) + '_' + difficulty
                if 71 <= contest <= 72:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 10).zfill(3) + '_' + difficulty
                if contest == 74:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 9).zfill(3) + '_' + difficulty
                if 77 <= contest <= 78:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 7).zfill(3) + '_' + difficulty
                if 81 <= contest <= 83:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 5).zfill(3) + '_' + difficulty
                if 86 <= contest <= 87:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 3).zfill(3) + '_' + difficulty
                if 90 <= contest <= 95:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest + 1).zfill(3) + '_' + difficulty
                if 97 <= contest <= 98:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest).zfill(3) + '_' + difficulty
                if 101 <= contest <= 102:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest - 2).zfill(3) + '_' + difficulty
                if 107 <= contest <= 108:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest - 6) + '_' + difficulty
                if contest == 111:
                    difficulty = transform_difficulty(difficulty)
                    last_path = 'arc' + str(contest - 8) + '_' + difficulty

                problem_url = 'https://atcoder.jp/contests/abc' + str(contest).zfill(3) + '/tasks/' + last_path

                html = requests.get(problem_url, headers=Data.UA)
                soup = BeautifulSoup(html.content, 'html.parser')

                self.contest_list.append(contest)
                self.statement_list.append(soup.find('section').text)

            print('contest' + str(contest) + ': completed!')

        self._sql.set_problems_data(len(self.title_list), self.contest_list, self.difficulty_list, self.title_list, self.statement_list)


def transform_difficulty(difficulty):
    if difficulty == 'c':
        difficulty = 'a'
    elif difficulty == 'd':
        difficulty = 'b'
    return difficulty
