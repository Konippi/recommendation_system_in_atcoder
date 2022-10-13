from dataset.src.service import scraping
from dataset.data import make_csv
import time


class Process:
    def __init__(self):
        self._users = scraping.Users()
        self._submissions = scraping.Submissions()
        self._problems = scraping.Problems()
        self._to_csv = make_csv.Csv()

    def make_csv(self):
        if input('Do you want to make the csvfile? (y/n) > ') == 'y':
            self._to_csv.make_csv()

    def collect_info(self):
        self._users.collect_users()
        self._submissions.collect_submissions()
        self._problems.collect_problems()
        self.make_csv()


def main():
    _process = Process()
    _process.collect_info()

    # timer end
    time_end = time.time()
    print('----------')
    print('Time: {:.2f}[s]'.format(time_end-time_start))
    print('----------')


if __name__ == '__main__':
    # timer start
    time_start = time.time()
    main()
