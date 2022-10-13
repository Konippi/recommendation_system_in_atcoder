import mysql.connector


class Sql:
    def __init__(self):
        self.userName = 'root'
        self.password = 'root'
        self.host = 'localhost'
        self.dbName = 'research_dataset'
        self.cur = None
        self.conn = None

    def connect_db(self):
        cur = None
        conn = None

        try:
            conn = mysql.connector.connect(
                user=self.userName,
                password=self.password,
                host=self.host,
                db=self.dbName
            )

            cur = conn.cursor()

        except Exception as e:
            print('----------')
            print('Error Occurred in the middle of connecting db: {}'.format(e))
            print('----------\n')

        finally:
            if conn is not None and conn.is_connected():
                self.cur = cur
                self.conn = conn

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def truncate(self, table_name):
        self.connect_db()

        sql1 = 'SET FOREIGN_KEY_CHECKS = 0'
        sql2 = 'TRUNCATE TABLE {}'
        sql3 = 'SET FOREIGN_KEY_CHECKS = 1'

        self.cur.execute(sql1)
        self.cur.execute(sql2.format(table_name))
        self.cur.execute(sql3)

        self.close_db()
        print('\"' + table_name + '\" table is truncated successfully!')

    def set_users_data(self, user_num, user_list, rating_list):
        self.connect_db()

        sql = 'INSERT INTO users(user_name, user_rating) VALUES(%s, %s)'

        for i in range(user_num):
            users_info = [user_list[i], rating_list[i]]
            try:
                self.cur.execute(sql, users_info)

            except mysql.connector.Error as e:
                print('Something went wrong: ' + str(e))

        self.close_db()

    def get_users_data(self, user_num):
        self.connect_db()

        user_list = []

        sql = 'SELECT user_name FROM users'

        try:
            self.cur.execute(sql)
            user_data = self.cur.fetchall()
            for i in range(user_num):
                user_list.append(user_data[i][0])

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        return user_list

    def get_user_details(self):
        self.connect_db()

        user_details = []

        sql = 'SELECT user_name, user_rating FROM users'

        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for result in results:
                user_details.append(list(result))

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        return user_details

    def get_now_contest(self):
        self.connect_db()

        sql = 'SELECT contest_num FROM submissions ORDER BY contest_num DESC'

        result = None

        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()[0][0]

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        if result is None:
            return 1
        else:
            return result

    def is_existed(self, contest):
        self.connect_db()

        sql = 'SELECT * FROM submissions WHERE contest_num = ' + str(contest)

        result = None

        try:
            self.cur.execute(sql)
            result = len(self.cur.fetchall())

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        return result > 0

    def set_submissions_data(self, data_num, user_name_list, date_list, contest_list,
                             problem_difficulty_list, problem_title_list, language_list,
                             status_list, code_length_list, runtime_list, memory_usage_list):
        self.connect_db()

        sql = 'INSERT INTO submissions(' \
              'user_name,' \
              'date,' \
              'contest_num,' \
              'problem_difficulty,' \
              'problem_title,' \
              'language,' \
              'status,' \
              'code_len,' \
              'runtime,' \
              'memory_usage) ' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        for i in range(data_num):
            submissions_info = [user_name_list[i], date_list[i], contest_list[i], problem_difficulty_list[i],
                                problem_title_list[i], language_list[i], status_list[i], code_length_list[i],
                                runtime_list[i], memory_usage_list[i]]
            try:
                self.cur.execute(sql, submissions_info)

            except mysql.connector.Error as e:
                print('Something went wrong: ' + str(e))

        print('complete!')

        self.close_db()

    def get_submission_details(self):
        self.connect_db()

        submission_details = []

        sql = 'SELECT user_name, date, contest_num, problem_difficulty, problem_title, language, ' \
              'status, code_len, runtime, memory_usage ' \
              'FROM submissions'

        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for result in results:
                submission_details.append(list(result))

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        return submission_details

    def set_problems_data(self, problem_num, contest_list, difficulty_list, title_list, statement_list):
        self.connect_db()

        sql = 'INSERT INTO problems(contest, difficulty, title, statement) VALUES(%s, %s, %s, %s)'

        for i in range(problem_num):
            problems_info = [contest_list[i], difficulty_list[i], title_list[i], statement_list[i]]
            try:
                self.cur.execute(sql, problems_info)

            except mysql.connector.Error as e:
                print('Something went wrong: ' + str(e))

        self.close_db()

    def get_problem_details(self):
        self.connect_db()

        problem_details = []

        sql = 'SELECT contest, difficulty, title, statement FROM problems'

        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for result in results:
                problem_details.append(list(result))

        except mysql.connector.Error as e:
            print('Something went wrong: ' + str(e))

        self.close_db()

        return problem_details
