from getpass import getpass

from src import Main


class Worker:
    def __init__(self):
        self.worker_id = None
        self.conn = Main.create_connection()

    def worker_login(self):
        email = input("Enter Email Id: ")
        sql = "SELECT email,password,id FROM Employees WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()
        if record:
            if record[1] is None:
                password = getpass('First time Login. Enter Password: ')
                sql = "Update Employees SET password = '{}' WHERE id = {}".format(password, record[2])
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                self.worker_id = record[2]
                return True
            else:
                password = getpass('Enter Password: ')
                if record[1] == password:
                    print("Authentication Successful")
                    self.worker_id = record[2]
                    return True
                else:
                    print("Authentication failed. Please check your credentials")
                    return False
        else:
            print("User does not exist")
            return False

    def worker_tasks(self):
        try:
            print("\nMenu\n"
                  "1: Create Complaint\n"
                  "2: Show Complaint History\n"
                  "3: Show Active Complaints\n"
                  "4: Show Profile\n"
                  "5: Exit\n")
            option = int(input("Select option: "))

            if option == 1:
                Worker.create_complaint(self)
            elif option == 2:
                Worker.show_complaint_history(self)
            elif option == 3:
                Worker.show_active_complaints(self)
            elif option == 4:
                Worker.show_worker_profile(self)
            elif option == 5:
                print("Thank You")
                exit()
            else:
                raise Exception
        except Exception as e:
            print("Invalid Choice. Please select again!")
            Worker.worker_tasks(self)

    def create_complaint(self):
        try:
            accident_name = input("Enter details: ")
            comments = input("Enter comments: ")

            sql = """INSERT INTO Complaints (accident_name, comments, worker_id)
                                VALUES ('{}','{}',{})""".format(accident_name, comments, self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            print("Complaint created successfully!")
            return True
        except Exception as e:
            print("Error is", e)
            return False
        finally:
            Worker.worker_tasks(self)

    def show_complaint_history(self):
        try:
            sql = "select * from Complaints where worker_id = {}".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("id : {}".format(i[0]))
                print("Accident_name : {}".format(i[1]))
                print("Comments : {}".format(i[2]))
                print("Status : {}".format(i[4]))
                print("----------------------------")


        except Exception as e:
            print("Error in reading data")
        finally:
            Worker.worker_tasks(self)

    def show_active_complaints(self):
        try:
            sql = "select * from Complaints where worker_id = {} and status = 'WIP'".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Complaint_id : {}".format(i[0]))
                print("Accident_name : {}".format(i[1]))
                print("Comments : {}".format(i[2]))
                print("Status : {}".format(i[4]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")
        finally:
            Worker.worker_tasks(self)

    def show_worker_profile(self):
        try:
            sql = "select * from Employees where id = {}".format(self.worker_id)
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Employee_id : {}".format(i[0]))
                print("Name : {}".format(i[1]))
                print("Email : {}".format(i[2]))
                print("Role : {}".format(i[4]))
                print("----------------------------")
        except Exception as e:
            print("Error in reading data")
        finally:
            Worker.worker_tasks(self)
