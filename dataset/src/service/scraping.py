import time

from dataset.src.service import db
from dataset.csv import make_csv

import requests
import re
from bs4 import BeautifulSoup


class Data:
    UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    userList = []
    next_contest = 1
    latest_contest = 1
    _sql = db.Sql()
    _toCsv = make_csv.Csv()


class Users(Data):
    def __init__(self):
        self.ranking_url = 'https://atcoder.jp/ranking?page='
        self.page = 0
        self.user_num = 1000
        self.userList = []
        self.ratingList = []

    def collect_users(self):
        print('----------')
        print('Start collecting user\'s info')
        print('----------')

        # truncate user's data
        if input('Do you want truncate the user\'s data? (y/n) > ') == 'y':
            Data._sql.truncate('Users')
        else:
            Data.userList = self._sql.get_users_data(self.user_num)
            return

        # top 1000 user's data
        for page_num in range(self.user_num // 100):
            html = requests.get(self.ranking_url + str(page_num + 1), headers=Data.UA)
            soup = BeautifulSoup(html.content, 'html.parser')

            # userName
            for name in soup.find_all('a', class_=re.compile('username')):
                self.userList.append(name.text)

            # rating
            judge_rating = 0
            for rating in soup.findAll('b'):
                if judge_rating % 2 == 0:
                    self.ratingList.append(int(rating.text))
                judge_rating += 1

            self.page += 1

            print(str(100 * self.page) + ' users: complete!')

            time.sleep(0.5)

        Data._sql.set_users_data(self.user_num, self.userList, self.ratingList)
        Data.userList = self.userList


class Submissions(Data):
    def __init__(self):
        self.data_num = 0
        self.userNameList = []
        self.dateList = []
        self.contestList = []
        self.problemList = []
        self.languageList = []
        self.statusList = []
        self.codeLengthList = []
        self.runtimeList = []
        self.memoryUsageList = []
        self.database = db.Sql()

    # clear
    def initialization(self):
        self.data_num = 0
        self.userNameList.clear()
        self.dateList.clear()
        self.contestList.clear()
        self.problemList.clear()
        self.languageList.clear()
        self.statusList.clear()

    def collect_submissions(self):
        # latest contest
        contest_url = 'https://atcoder.jp/contests/archive?ratedType=1&category=0'
        html = requests.get(contest_url, headers=Data.UA)
        soup = BeautifulSoup(html.content, 'html.parser')
        Data.latest_contest = int(soup.find(href=re.compile('/contests/abc')).text[25:])

        print('\n----------')
        print('Start collecting submission\'s info')
        print('----------')

        # truncate submission's data
        if input('Do you want truncate the submission\'s data? (y/n) > ') == 'y':
            Data._sql.truncate('Submissions')
        else:
            Data.next_contest = int(self._sql.get_now_contest()) + 1
            if Data.next_contest == Data.latest_contest + 1:
                if input('Do you want make the csvfile? (y/n) > ') == 'y':
                    Data._toCsv.make_csv()
                return

        # Contest: now contest - latest contest
        for contest in range(Data.next_contest, Data.latest_contest + 1):
            print('\n----- ABC' + str(contest) + ' -----\n')

            # initialization
            self.initialization()

            # the existed contest
            if self._sql.is_existed(contest):
                print('already existed!')
                continue

            for user in Data.userList:
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
                    self.dateList.append(date[:19])

                    # problem
                    problem = data.find(href=re.compile(r'/tasks/')).text
                    self.problemList.append(problem)

                    # user
                    self.userNameList.append(user)

                    # language
                    language = data.find(href=re.compile(r'Language=')).text
                    self.languageList.append(language)

                    # status
                    status = data.find('span', class_=re.compile('label-')).text
                    self.statusList.append(status)

                    # codeLength, runtime, memoryUsage
                    detail_num = 0
                    for detail in data.find_all('td', class_='text-right'):
                        # codeLength
                        if detail_num == 1:
                            code_length = detail.text
                            self.codeLengthList.append(code_length)

                        # CE process
                        if status == 'CE' and detail_num == 1:
                            self.runtimeList.append(str(0) + 'ms')
                            self.memoryUsageList.append(str(0) + 'KB')
                            continue

                        # runtime
                        if detail_num == 2:
                            runtime = detail.text
                            self.runtimeList.append(runtime)

                        # memoryUsage
                        if detail_num == 3:
                            memory_usage = detail.text
                            self.memoryUsageList.append(memory_usage)

                        detail_num += 1

                    # contest
                    self.contestList.append(str(contest).zfill(3))

                    # data_num
                    self.data_num += 1

                time.sleep(0.5)

            Data._sql.set_submissions_data(self.data_num, self.userNameList, self.dateList,
                                           self.contestList, self.problemList, self.languageList,
                                           self.statusList, self.codeLengthList, self.runtimeList,
                                           self.memoryUsageList)
