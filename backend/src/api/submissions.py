import requests
from datetime import datetime

def get_submissions(user_name: str):
    res = requests.get('https://kenkoooo.com/atcoder/atcoder-api/results?user={}'.format(user_name))
    submissions = eval(res.text.replace('null', '\"null\"'))
    submissions_info_by_contest = {}

    for contest in range(1, 251):
        submissions_info_by_contest[str(contest)] = []

    for submission in submissions:
        # convert unix time to datetime
        date = str(datetime.fromtimestamp(submission['epoch_second'])).replace('T', ' ')

        # only abc
        if submission['problem_id'][:3] != 'abc':
            continue

        problem_info = submission['problem_id'].split('_')
        contest = problem_info[0][3:].lstrip('0')

        # contest <= 250
        if int(contest) > 250:
            continue

        problem = problem_info[1]
        problem = problem[0].upper() + problem[1:]

        # convert 'H' to 'Ex'
        if int(contest) >=  233 and problem == 'H':
            problem = 'Ex'

        # convert digit to alphabet
        if problem.isdigit():
            problem = chr(64 + int(problem))

        result = submission['result']
        submissions_info_by_contest[contest].append(
            {
                'date': date,
                'problem': problem,
                'result': result
            }
        )

    return submissions_info_by_contest