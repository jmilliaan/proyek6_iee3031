from roboconvcv_database import DBConnection

db = DBConnection()

db.execute_commit("INSERT INTO command(command, sequence) VALUES(1, 1)")

db.execute_commit("INSERT INTO command(command, sequence) VALUES(1, 2)")
