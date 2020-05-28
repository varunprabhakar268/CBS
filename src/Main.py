from src import EmployeeService, schema,AdminService
import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
    db_file = "cbs_db.sqlite"
    try:
        conn = sqlite3.connect(db_file)
        schema.create_tables(conn)
        sql = "PRAGMA foreign_keys = ON"
        cur = conn.cursor()
        cur.execute(sql)
        return conn
    except Error as e:
        print(e)


if __name__ == '__main__':
    ch = ''
    num = 0
    conn = create_connection()

    while ch != '3':

        print("MAIN MENU")
        print("1. Admin Login")
        print("2. Employee Login")
        print("3. Exit")
        ch = input("Select Your Option ")

        if ch == '1':
            admin = AdminService.Admin()
            if admin.admin_login():
                admin.admin_tasks()
        elif ch == '2':
            employee = EmployeeService.Employee()
            if employee.employee_login():
                employee.employee_tasks()

        elif ch == '3':
            print("Thank You.")
        else:
            print("Invalid choice")
