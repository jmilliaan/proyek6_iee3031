from roboconvcv_database import DBConnection

db = DBConnection()

db.execute_commit("INSERT INTO command(command, sequence) VALUES(0, 1)")

db.execute_commit("INSERT INTO command(command, sequence) VALUES(1, 2)")
