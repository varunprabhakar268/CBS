from getpass import getpass
from src import Main


class Supervisor:

    def __init__(self):
        self.TeamName = None
        self.supervisor_id = None
        self.conn = Main.create_connection()

    def supervisor_login(self):
        """
        supervisor authentication.
        :return:
        """
        email = input("Enter Email Id: ")
        sql = "SELECT email,password,id,TeamName FROM Supervisors WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()
        if record:
            if record[1] is None:
                password = getpass('First time Login. Enter Password: ')
                sql = "Update Supervisors SET password = '{}' WHERE id = {}".format(password, record[2])
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                self.supervisor_id = record[2]
                return True
            else:
                password = getpass('Enter Password: ')
                if record[1] == password:
                    print("Authentication Successful")
                    self.supervisor_id = record[2]
                    self.TeamName = record[3]
                    return True
                else:
                    print("Authentication failed. Please check your credentials")
                    return False
        else:
            print("User does not exist")
            return False

    def supervisor_tasks(self):
        """
        show supervisor tasks.
        :return:
        """
        try:
            print("\nMenu\n"
                  "1: Show Complaint\n"
                  "2: Create Report\n"
                  "3: Show Reports\n"
                  "4: Exit\n")
            option = int(input("Select option: "))

            if option == 1:
                Supervisor.show_complaint(self)
                Supervisor.supervisor_tasks(self)
            elif option == 2:
                Supervisor.create_report(self)
            elif option == 3:
                Supervisor.show_reports(self)
            elif option == 4:
                print("Thank You")
                exit()
            else:
                raise Exception

        except Exception as e:
            print("Invalid Choice. Please select again!")
            Supervisor.supervisor_tasks(self)

    def show_complaint(self):
        """
        show complaint details.
        :return:
        """
        try:
            sql = "select c.id,c.accident_name,c.comments from Complaints c where assigned_team = '{}'".format(
                self.TeamName)
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Complaint_id : {}".format(i[0]))
                print("Accident Name : {}".format(i[1]))
                print("Comments : {}".format(i[2]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")

    def create_report(self):
        """
        create new report.
        :return:
        """
        try:
            Supervisor.show_complaint(self)
            complaint_no = int(input("Enter Complaint id: "))
            root_cause = input("Enter root cause: ")
            details = input("Enter details: ")
            affected = int(input("Enter the total number of people affected: "))
            casualties = int(input("Enter the total number casualties: "))

            sql = """INSERT INTO Report (complaint_id,TeamName,root_cause,details,no_of_people_affected,no_of_casualties)
                                VALUES ({},'{}','{}','{}',{},{})""".format(complaint_no, self.TeamName, root_cause,
                                                                           details, affected, casualties)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            print("Report submitted successfully!")
        except Exception as e:
            print("Error is", e)
        finally:
            Supervisor.supervisor_tasks(self)

    def show_reports(self):
        """
        show report details.
        :return:
        """
        try:
            sql = "select * from Report where TeamName = '{}'".format(self.TeamName)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                result = cur.fetchall()
            for i in result:
                print("Report Id : {}".format(i[0]))
                print("Root Cause : {}".format(i[3]))
                print("Details : {}".format(i[4]))
                print("Affected Count : {}".format(i[5]))
                print("Casualty Count : {}".format(i[6]))
                print("Status : {}".format(i[7]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")
        finally:
            Supervisor.supervisor_tasks(self)
