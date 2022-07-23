from dataset.src.service import scraping
import time


class Process:
    def __init__(self):
        self._users = scraping.Users()
        self._submissions = scraping.Submissions()

    def collect_info(self):
        self._users.collect_users()
        self._submissions.collect_submissions()


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
