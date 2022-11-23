import random
import time

import requests
from bs4 import BeautifulSoup
import csv
import re

def scraping():
    result_list = []
    name_list = []
    rate_list = []

    for page in range(1,3):
        url = 'https://atcoder.jp/ranking/all?contestType=algo&f.RatingLowerBound=0' \
              '&f.RatingUpperBound=100&f.CompetitionsLowerBound=30&page=' + str(page)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        for user_name in soup.findAll('span', class_=re.compile(r'user-')):
            name_list.append(user_name.text)

        rate_cnt = 0
        for rate in soup.findAll('b'):
            if rate_cnt % 2 == 0:
                rate_list.append(rate.text)
            rate_cnt += 1

        print('page' + str(page) + ': complete!')

    for i in range(len(name_list)):
        result_list.append([name_list[i], rate_list[i]])

    with open('csv/test_user0_100.csv', 'w', newline='', errors='ignore') as f_test:
        writer = csv.writer(f_test)
        for row in result_list:
            writer.writerow(row)

if __name__ == '__main__':
    scraping()