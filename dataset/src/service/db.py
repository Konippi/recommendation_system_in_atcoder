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
        print('----------')
        print('Start db connections')
        print('----------\n')

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

    def is_exist_user_table(self):
        self.connect_db()

        sql = 'SELECT COUNT(*) FROM Users'
        self.cur.execute(sql)
        user_num = int(self.cur.fetchall()[0][0])

        if user_num == 10000:
            print('----------')
            print('User table already exists')
            print('----------\n')
            return True

        return False

    def set_data(self, users, ratings):
        self.connect_db()

        sql = 'INSERT INTO Users(user_name, user_rating) VALUES(%s, %s)'

        for i in range(10000):
            user_info = [users[i], ratings[i]]
            try:
                self.cur.execute(sql, user_info)
                print('(user: ' + users[i] + ', rating: ' + str(ratings[i]) + ')')

            except mysql.connector.Error as e:
                print('Something went wrong: {}'.format(e))

        self.close_db()
