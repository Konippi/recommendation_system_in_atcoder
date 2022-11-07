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

    def calc(self, submission_info: list):
        self._calc.calc(submission_info=submission_info)

@app.get('/{user_name}')
def get_recommended_problems(user_name: str):
    user = User()
    submission_info = user.get_submissions_info(user_name=user_name)
    _process = Process()
    _process.calc(submission_info=submission_info)
    return {
        'api_response': {
            'submission_info': submission_info,
            'recommended_problems': Data.recommended_problem_dict_list
        }
    }

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
