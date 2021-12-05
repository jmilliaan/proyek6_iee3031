import mysql.connector
import roboconvcv_constants as constants


class DBConnection:
    def __init__(self):
        self.host_ip = constants.mysql_ip
        self.user = constants.mysql_username
        self.password = constants.mysql_password
        self.mydb = mysql.connector.connect(host=self.host_ip,
                                            user=self.user,
                                            password=self.password)
        self.c = self.mydb.cursor()
        print("Connected to MySQL Server at:", self.host_ip, "\nAs user:", self.user)

    def commit(self):
        self.mydb.commit()

    def execute(self, query):
        self.c.execute(query)

    def execute_commit(self, query):
        self.c.execute(query)
        self.commit()

    def print_c(self):
        for i in self.c.fetchall():
            print(i)

    def reconnect(self):
        self.mydb = mysql.connector.connect(host=constants.mysql_ip,
                                            user=constants.mysql_username,
                                            password=constants.mysql_password)
        self.c = self.mydb.cursor()
