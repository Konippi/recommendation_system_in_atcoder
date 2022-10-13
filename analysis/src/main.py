from service import calc
from fastapi import FastAPI

app = FastAPI()


class Process:
    def __init__(self):
        self._calc = calc.Calc()

    def calc(self):
        self._calc.calc()


@app.get('/')
def main():
    _process = Process()
    _process.calc()


if __name__ == '__main__':
    main()