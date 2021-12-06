import mysql.connector
import roboconvcv_constants as constants
from datetime import datetime


class DBConnection:
    def __init__(self):
        self.host_ip = constants.mysql_ip
        self.user = constants.mysql_username
        self.password = constants.mysql_password
        self.connected = False
        self.table_name = "event_logging"

        try:
            self.mydb = mysql.connector.connect(host=self.host_ip,
                                                user=self.user,
                                                password=self.password)
            self.c = self.mydb.cursor()
            print("Connected to MySQL Server at:", self.host_ip, "\nAs user:", self.user)
            self.execute_commit("USE Proyek6_IEE3031;")
            self.connected = True

        except:
            print("Failed To Connect to DB.")
            self.connected = False
            pass

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d-%m-%Y")

    def commit(self):
        if self.connected:
            self.mydb.commit()

    def execute(self, query):
        if self.connected:
            self.c.execute(query)

    def execute_commit(self, query):
        if self.connected:
            self.execute("USE Proyek6_IEE3031;")
            self.c.execute(query)
            self.commit()

    def log_start_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Conveyor starting.")

    def log_slow_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(),
                     "Item near grabbing position. "
                     "Conveyor Belt slowing down.")

    def log_stop_conv(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Item at grabbing position. Conveyor stopping.")

    def log_ssc_take_item(self):
        if self.connected:
            self.log(self.get_time(), self.get_date(), "Item at grabbing position. SSC32 Robot Arm taking object.")

    def log(self, current_time, current_date, event):
        if self.connected:
            self.execute_commit(f"INSERT INTO {self.table_name}"
                                f"(time, date, event) "
                                f"VALUES({current_time}, {current_date}, {event});")

    def print_c(self):
        if self.connected:
            for i in self.c.fetchall():
                print(i)
        else:
            pass

    def reconnect(self):
        try:
            self.mydb = mysql.connector.connect(host=constants.mysql_ip,
                                                user=constants.mysql_username,
                                                password=constants.mysql_password)
            self.c = self.mydb.cursor()
            self.connected = True
        except:
            print("Failed to Reconnect to DB.")
            self.connected = False
            pass
