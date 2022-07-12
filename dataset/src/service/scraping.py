from dataset.src.service import db

import requests
import re
from bs4 import BeautifulSoup


class Data:
    userList = []


class Users(Data):
    def __init__(self):
        self.ranking_url = 'https://atcoder.jp/ranking?page='
        self.userList = []
        self.ratingList = []
        self.sql = db.Sql()

    def collect_users(self):
        print('----------')
        print('Start collecting user\'s info')
        print('----------\n')

        # truncate user's data
        self.sql.truncate('Users')

        # top 10000 user's data
        for page_num in range(100):
            html = requests.get(self.ranking_url + str(page_num + 1))
            soup = BeautifulSoup(html.content, 'html.parser')

            for name in soup.find_all('a', class_=re.compile('username')):
                self.userList.append(name.text)

            is_rating = 0

            for rating in soup.findAll('b'):
                if is_rating % 2 == 0:
                    self.ratingList.append(int(rating.text))
                is_rating += 1

        self.sql.set_user_data(self.userList, self.ratingList)
        Data.userList = self.userList


class Submissions(Data):
    def __init__(self):
        self.submission_url = ''
        self.userNameList = []
        self.dataList = []
        self.contestNameList = []
        self.statusList = []
        self.codeLengthList = []
        self.memoryUsageList = []
        self.database = db.Sql()

    def collect_submissions(self):
        print('----------')
        print('Start collecting submission\'s info')
        print('----------\n')

        # Contest: 1 - 200
        for contest in range(1, 201):
            for user in Data.userList:
                self.submission_url = 'https://atcoder.jp/contests/abc' + str(contest) + '/submissions?f.User=' + user
                print(self.submission_url)


