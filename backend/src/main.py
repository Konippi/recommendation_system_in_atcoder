from service import calc
from backend.src.metadata.data import Data
from fastapi import FastAPI

app = FastAPI()

class Process(Data):
    def __init__(self):
        self._calc = calc.Calc()

    def calc(self, contest, problem):
        Data.test_problem = [contest, problem]
        self._calc.calc()


@app.get('/')
def main(contest, problem):
    _process = Process()
    _process.calc(contest, problem)

    return {'recommend_problems': Data.recommend_problem_dict_list}
