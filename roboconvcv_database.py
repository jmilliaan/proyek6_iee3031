import mysql.connector
import roboconvcv_constants as constants
from datetime import datetime


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
        self.execute_commit("USE Proyek6_IEE3031;")
        self.table_name = "event_logging"

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d-%m-%Y")

    def commit(self):
        self.mydb.commit()

    def execute(self, query):
        self.c.execute(query)

    def execute_commit(self, query):
        self.c.execute(query)
        self.commit()

    def log_start_conv(self):
        self.log(self.get_time(), self.get_date(), "Conveyor starting.")

    def log_slow_conv(self):
        self.log(self.get_time(), self.get_date(), "Item near grabbing position. Conveyor Belt slowing down.")

    def log_stop_conv(self):
        self.log(self.get_time(), self.get_date(), "Item at grabbing position. Conveyor stopping.")

    def log_ssc_take_item(self):
        self.log(self.get_time(), self.get_date(), "Item at grabbing position. SSC32 Robot Arm taking object.")

    def log(self, current_time, current_date, event):
        self.execute_commit(f"INSERT INTO {self.table_name}"
                            f"(time, date, event) "
                            f"VALUES({current_time}, {current_date}, {event});")

    def print_c(self):
        for i in self.c.fetchall():
            print(i)

    def reconnect(self):
        self.mydb = mysql.connector.connect(host=constants.mysql_ip,
                                            user=constants.mysql_username,
                                            password=constants.mysql_password)
        self.c = self.mydb.cursor()
