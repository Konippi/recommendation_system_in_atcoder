from dataset.src.service import scraping
from dataset.src.service import db


class Process:
    def __init__(self):
        # instance of Sql
        self.database = db.Sql()

        # instance of User
        self.user = scraping.User()

    def get_info(self):
        if not self.database.is_exist_user_table():
            self.user.get_userinfo()

        # instance of Problem


def main():
    process = Process()
    process.get_info()


if __name__ == '__main__':
    main()
