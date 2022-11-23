import asyncio
import csv
import sys
sys.path.append('../../')
from backend.src.api import submissions
import requests

args = sys.argv
result_list = []

def get_test_users():
    user_info_list = []
    with open('data/csv/test_user0_100.csv', 'r', encoding='utf-8') as test_f:
        reader = csv.reader(test_f)
        for row in reader:
            user_info_list.append(row)
    return user_info_list

def convert_diff(diff: str):
    if diff == 'A':
        return 1
    elif diff == 'B':
        return 2
    elif diff == 'C':
        return 3
    elif diff == 'D':
        return 4
    elif diff == 'E':
        return 5
    elif diff == 'F':
        return 6
    elif diff == 'G':
        return 7
    else:
        return 8

async def get_recommended_problems(user):
    url = 'http://localhost:8000/' + user[0]
    converted_res = eval(requests.get(url).text)
    res = converted_res['api_response']['recommended_problems']

    # no recommended problems
    if len(res) == 0:
        return 'null', 'null', 'null'

    diff_num_list = []
    diff_str = res[0]['problem']['diff']
    for res_info in res:
        diff_num_list.append(convert_diff(res_info['problem']['diff']))
    diff_num = sum(diff_num_list)/len(diff_num_list)
    rate = user[1]
    return rate, diff_str, diff_num

async def create_result(user_info):
    rate, diff_str, diff_num = await get_recommended_problems(user_info)
    result_list.append([rate, diff_str, diff_num])

if __name__ == '__main__':
    test_user_list = get_test_users()

    if args[1] == 'test1':
        for test_user in test_user_list:
            asyncio.run(create_result(test_user))

        with open('data/csv/result0_100.csv', 'w', newline='', errors='ignore') as f:
            writer = csv.writer(f)

        for result in result_list:
            writer.writerow(result)

    elif args[1] == 'test2':
        for test_user in test_user_list:
            submissions_info_list = submissions.get_submissions(test_user[0])
            ac_date_list = []
            for contest, submissions in submissions_info_list.items():
                for submission in submissions:
                    if submission['result'] == 'AC':
                        ac_date_list.append(submission['date'])

            ac_date_list.reverse()
            exclude_date_list = ac_date_list[:5]


            # url = 'http://localhost:8000/recommend'
            # params = {'submissions_info_list': }
            # converted_res = eval(requests.get(url, params=params).text)
            # res = converted_res['api_response']['recommended_problems']

            # converted_submissions = sorted(submissions_info_list,
            #                                key=lambda data:data['submissions']['date'],
            #                                reverse=True)
            # print(converted_submissions)
