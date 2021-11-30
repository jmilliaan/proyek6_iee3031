import mysql.connector

class DBConnection:
    def __init__(self):
        self.host_ip = "10.252.242.117"
        self.user = "jm_03"
        self.password = "iee3031"
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
        self.mydb = mysql.connector.connect(host="10.252.242.117",
                                            user="jm_03",
                                            password="iee3031")
        self.c = self.mydb.cursor()

    