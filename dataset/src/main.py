from dataset.src.service import scraping
from dataset.src.service import db


class Process:
    def __init__(self):
        # instance of Sql
        self.database = db.Sql()

        # instance of Users
        self.user = scraping.Users()

        # instance of Problems
        self.submission = scraping.Submissions()

    def get_info(self):
        self.user.get_users()
        self.submission.get_submissions()


def main():
    process = Process()

    process.get_info()


if __name__ == '__main__':
    main()
