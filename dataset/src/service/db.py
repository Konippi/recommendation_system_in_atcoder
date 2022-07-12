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

    def truncate(self, table_name):
        self.connect_db()

        sql1 = 'SET FOREIGN_KEY_CHECKS = 0'
        sql2 = 'TRUNCATE TABLE {}'
        sql3 = 'SET FOREIGN_KEY_CHECKS = 1'

        self.cur.execute(sql1)
        self.cur.execute(sql2.format(table_name))
        self.cur.execute(sql3)

        self.close_db()

    def set_user_data(self, users, ratings):
        self.connect_db()

        sql = 'INSERT INTO Users(user_name, user_rating) VALUES(%s, %s)'

        for i in range(10000):
            user_info = [users[i], ratings[i]]
            try:
                self.cur.execute(sql, user_info)
                print('(user: ' + users[i] + ', rating: ' + str(ratings[i]) + ')')

            except mysql.connector.Error as e:
                print('Something went wrong: ' + e)

        self.close_db()
