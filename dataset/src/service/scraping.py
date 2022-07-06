from dataset.src.service import db

import requests
import re
from bs4 import BeautifulSoup


class User:
    def __init__(self):
        self.ranking_url = 'https://atcoder.jp/ranking?page='
        self.userList = []
        self.ratingList = []
        self.database = db.Sql()

    def get_userinfo(self):
        print('----------')
        print('Start collecting atcoder\'s info')
        print('----------\n')

        # top 10000 user's datas
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

        self.database.set_data(self.userList, self.ratingList)


class Problem:
    pass
