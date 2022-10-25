class Data:
    # List #
    user_list = []  # 100

    filter_user_list = []  # 73

    submission_list = []  # 39189

    problem_list = []  # 1328

    test_vec = []

    test_problem = []

    recommend_problem_dict_list = []

    # Dict #
    # {user: rating}
    rating_dict = {}

    # {user: submission_num}
    submission_num_dict = {}

    # {user: [[date, contest, problem, state],[date,...]}
    submission_by_user_dict = {}

    # Num #
    ave_submission_num = None
