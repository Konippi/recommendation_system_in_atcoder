from src import ac


class Process:
    def __init__(self):
        self._ac = ac.Ac()

    def calc(self):
        self._ac.calc_ratio_ac()


def main():
    _process = Process()
    _process.cal_ratio_ac()


if __name__ == '__main__':
    main()
