from src import ac


class Process:
    def __init__(self):
        self._ac = ac.Ac()

    def cal_ratio_ac(self):
        self._ac.set_data()


def main():
    _process = Process()
    _process.cal_ratio_ac()


if __name__ == '__main__':
    main()
