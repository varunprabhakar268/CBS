from src import SupervisorService, WorkerService, schema,AdminService
import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
    db_file = "aims_db.sqlite"
    try:
        conn = sqlite3.connect(db_file)
        schema.create_tables(conn)
        # sql = "PRAGMA foreign_keys = ON"
        # cur = conn.cursor()
        # cur.execute(sql)
        return conn
    except Error as e:
        print(e)


if __name__ == '__main__':
    ch = ''
    num = 0
    conn = create_connection()

    while ch != 4:

        print("MAIN MENU")
        print("1. Admin Login")
        print("2. Supervisor Login")
        print("3. Worker Login")
        print("4. Exit")
        ch = input("Select Your Option ")

        if ch == '1':
            admin = AdminService.Admin()
            if admin.admin_login():
                admin.admin_tasks()
        elif ch == '2':
            supervisor = SupervisorService.Supervisor()
            if supervisor.supervisor_login():
                supervisor.supervisor_tasks()

        elif ch == '3':
            worker = WorkerService.Worker()
            if worker.worker_login():
                worker.worker_tasks()

        elif ch == '4':
            print("Thank You.")
            break
        else:
            print("Invalid choice")
