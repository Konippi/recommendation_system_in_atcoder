from dataset.metadata.data import Data
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor


def scraping(url):
    contest = url[31:34].lstrip('0')
    html = requests.get(url, headers=Data.UA)
    soup = BeautifulSoup(html.content, 'html.parser')
    submission_list_by_contest = []
    data_cnt = 0
    data_dict = dict()
    for data in soup.findAll('td'):
        if data_cnt == 0:
            # exclude timezone
            data_dict['date'] = data.text[:19]
        elif data_cnt == 1:
            data_dict['problem'] = data.text
        elif data_cnt == 6:
            data_dict['result'] = data.text
            # in the case of CE
            if data.text == 'CE':
                data_cnt = 8
        elif data_cnt % 9 == 0:
            submission_list_by_contest.append({
                'date': data_dict['date'],
                'problem': data_dict['problem'],
                'result': data_dict['result']
            })
            data_dict.clear()
            data_cnt = 0
            continue
        data_cnt += 1
    return {
        'contest': contest,
        'submissions': submission_list_by_contest
    }


class User(Data):
    def __init__(self):
        self.contest_num = Data.last_contest
        self.submission_list = []

    def get_submissions_info(self, user_name: str):
        urls = []

        for contest in range(1, self.contest_num+1):
            urls.append('https://atcoder.jp/contests/abc{}/submissions?f.User={}'
                        .format(str(contest).zfill(3), user_name))

        with ProcessPoolExecutor(max_workers=12) as executor:
            results = list(executor.map(scraping, urls))

        return results
