import time
from api import submissions
from service import calc
from service.user import User
from backend.src.metadata.data import Data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000']
)

class Process(Data):
    def __init__(self):
        self._calc = calc.Calc()

    def calc(self, submissions_info: list):
        self._calc.calc(submissions_info=submissions_info)

@app.get('/{user_name}')
def get_recommended_problems(user_name: str):
    start = time.time()
    # user = User()
    # submission_info = user.get_submissions_info(user_name=user_name)
    submissions_info_by_contest = submissions.get_submissions(user_name=user_name)

    submissions_info_list = []
    for contest in range(1, 251):
        submissions_info_list.append(
            {
                'contest': str(contest),
                'submissions': submissions_info_by_contest[str(contest)]
            }
        )

    _process = Process()
    _process.calc(submissions_info=submissions_info_list)

    end = time.time()
    print('runtime: {}s'.format(str(end-start)))

    return {
        'api_response': {
            'submissions_info': submissions_info_list,
            'recommended_problems': Data.recommended_problem_dict_list
        }
    }

@app.get('/recommend')
def get_recommended_problems(submissions_info_list: list[dict]):
    _process = Process()
    _process.calc(submissions_info=submissions_info_list)

    return {
        'recommended_problems': Data.recommended_problem_dict_list
    }

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
