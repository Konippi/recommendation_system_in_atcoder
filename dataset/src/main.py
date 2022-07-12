from dataset.src.service import scraping


class Process:
    def __init__(self):
        # instance of Users
        self.users = scraping.Users()

        # instance of Problems
        self.submissions = scraping.Submissions()

    def collect_info(self):
        self.users.collect_users()
        self.submissions.collect_submissions()


def main():
    process = Process()
    process.collect_info()


if __name__ == '__main__':
    main()
