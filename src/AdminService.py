
from getpass import getpass
from src import Main

from src import InputValidations


class Admin:

    def __init__(self):
        self.admin_id = None
        self.conn = Main.create_connection()

    def admin_login(self):
        """
        admin authentication
        :return:
        """
        email = input("Enter Email: ")

        sql = "SELECT email,password,id FROM Admin WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()
        if record:
            password = getpass('Enter Password: ')
            if record[1] == password:
                print("Authentication Successful")
                self.admin_id = record[2]
                return True
            else:
                print("Authentication failed. Please check your credentials")
                return False
        else:
            print("User does not exist")
            return False

    def admin_tasks(self):
        """
        show Admin Tasks.
        :return:
        """
        try:
            print("\nMenu\n"
                  "1: Worker Management\n"
                  "2: Supervisor Management\n"
                  "3: Show Complaints\n"
                  "4: Report Management\n"
                  "5: Exit\n")
            option = int(input("Select option: "))

            if option == 1:
                Admin.admin_worker_mgmnt(self)
            elif option == 2:
                Admin.admin_supervisor_mgmnt(self)
            elif option == 3:
                Admin.show_complaints(self)
                Admin.admin_tasks(self)
            elif option == 4:
                Admin.admin_report_management(self)
            elif option == 5:
                print("Thank You")
                exit()
            else:
                raise Exception

        except Exception as e:
            print("Invalid Choice. Please select again!")
            Admin.admin_tasks(self)

    def admin_worker_mgmnt(self):
        """
        worker management.
        :return:
        """
        try:
            print("\nMenu\n"
                  "1: Create Worker Profile\n"
                  "2: Show All Workers\n"
                  "3: Update Worker Profile\n"
                  "4: Delete Worker Profile\n"
                  "5: Assign Job Role\n"
                  "6: Go back\n")
            option = int(input("Select option: "))
            if option == 1:
                Admin.create_worker(self)
            elif option == 2:
                Admin.show_allworkers(self)
                Admin.admin_worker_mgmnt(self)
            elif option == 3:
                Admin.update_worker(self)
            elif option == 4:
                Admin.delete_worker(self)
            elif option == 5:
                Admin.assign_jobrole(self)
            elif option == 6:
                Admin.admin_tasks(self)
            else:
                raise Exception

        except Exception as e:
            print("Invalid Choice. Please select again!")
            Admin.admin_worker_mgmnt(self)

    def admin_supervisor_mgmnt(self):
        """
        supervisor management.
        :return:
        """
        try:
            print("\nMenu\n"
                  "1: Create Supervisor Team\n"
                  "2: Update Supervisor Profile\n"
                  "3: Delete Supervisor Profile\n"
                  "4: Delete Supervisor Team\n"
                  "5: Assign \n"
                  "6: Show All Supervisors \n"
                  "7: Back \n")
            option = int(input("Select task: "))
            if option == 1:
                Admin.create_supervisorTeam(self)
            elif option == 2:
                Admin.update_supervisor(self)
            elif option == 3:
                Admin.delete_supervisor(self)
            elif option == 4:
                Admin.delete_supervisor_team(self)
            elif option == 5:
                Admin.assign_supervisor(self)
            elif option == 6:
                Admin.show_allsupervisors(self)
                Admin.admin_supervisor_mgmnt(self)
            elif option == 7:
                Admin.admin_tasks(self)
            else:
                raise Exception

        except Exception as e:
            print("Invalid Choice. Please select again!")
            Admin.admin_supervisor_mgmnt(self)

    def admin_report_management(self):
        """
        report management.
        :return:
        """
        try:
            print("\nMenu\n"
                  "1: Show Report History\n"
                  "2: Show Approved Reports\n"
                  "3: Show Rejected Reports\n"
                  "4: Approve Pending Reports\n"
                  "5: Go back\n")
            option = int(input("Select task: "))
            if option == 1:
                Admin.show_all_reports(self)
            elif option == 2:
                Admin.show_approved_reports(self)
            elif option == 3:
                Admin.show_rejected_reports(self)
            elif option == 4:
                Admin.show_pending_reports(self)
            elif option == 5:
                Admin.admin_tasks(self)
            else:
                raise Exception
        except Exception as e:
            print("Invalid Choice. Please select again!")
            Admin.admin_report_management(self)

    def create_worker(self):
        """
        create a new worker.
        :return:
        """
        try:

            name = input("Enter name: ")
            if not name.isalpha():
                print("Invalid data format. Name should contain only alphabets. ")
                return False
            email = input("Enter email: ")
            if not InputValidations.validate_email(email):
                return False
            sql = """
                    INSERT INTO Employees (name,email)
                    VALUES ('{}','{}')
                  """.format(name,email)

            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                print("Worker created successfully!")

        except Exception as e:
            print("Error", e)
        finally:
            Admin.admin_worker_mgmnt(self)

    def get_worker_by_id(self, worker_id):
        """
        Get details of a particular worker.
        """

        sql = "SELECT name,email,role FROM Employees WHERE id = {}".format(worker_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()

        if record:
            print('''Name: {}\nEmail: {}\nRole: {}
                      '''.format(record[0], record[1], record[2]))
            return record
        else:
            print("Invalid Id")
            return False

    def update_worker(self):
        """
        update worker details.
        :return:
        """
        try:
            worker_id = int(input("Enter Worker Id "))
            record = self.get_worker_by_id(worker_id)
            if record:
                name = (input("Enter Updated Name or Enter to continue ") or record[0])
                if not name.isalpha():
                    print("Invalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue ") or record[1])
                if not InputValidations.validate_email(email):
                    return False
                role = (input("Enter Updated Role or Enter to continue ") or record[2])
                if not role.isalpha():
                    print("Invalid data format. Role should contain only alphabets.")
                    return False
                sql = ''' UPDATE Employees
                                  SET name = '{}' ,
                                      email = '{}' ,
                                      role = '{}'                      
                                  WHERE id = {}'''.format(name, email, role, worker_id)

                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                    self.conn.commit()

                print("Record Updated Successfully")
            record = self.get_worker_by_id(worker_id)

        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False
        finally:
            Admin.admin_worker_mgmnt(self)

    def delete_worker(self):
        """
        delete worker.
        :return:
        """
        try:
            Admin.show_allworkers(self)
            worker_id = int(input("Enter the Worker id: "))
            sql = 'DELETE FROM Employees WHERE id={}'.format(worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                print("Worker deleted successfully")

        except Exception as e:
            print("error", e)

        finally:
            Admin.admin_worker_mgmnt(self)

    def assign_jobrole(self):
        """
        assign role to worker.
        :return:
        """
        try:

            Admin.show_unassigned_workers(self)
            worker_id = int(input("Enter the worker id: "))
            role = input("Enter role: ")
            sql = 'UPDATE Employees SET role = "{}" WHERE id = {}'.format(role,worker_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
                print("Job role assigned")

        except Exception as e:
            print('error', e)

        finally:
            Admin.admin_worker_mgmnt(self)

    def show_allworkers(self):
        """
        show details of all workers.
        :return:
        """
        try:
            sql = "select * from Employees"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Worker Id : {}".format(i[0]))
                print("Name : {}".format(i[1]))
                print("Email : {}".format(i[2]))
                print("Role : {}".format(i[4]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")

    def show_unassigned_workers(self):
        """
        show details of unassigned workers.
        :return:
        """
        try:
            sql = "Select * from Employees where role = 'none' "
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Worker Id : {}".format(i[0]))
                print("Name : {}".format(i[1]))
                print("Email : {}".format(i[2]))
                print("Role : {}".format(i[4]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")

    def create_supervisorTeam(self):
        """
        create new supervision team.
        :return:
        """
        try:
            num = int(input("Enter number of members: "))
            team_name = input("Enter Team Name: ")
            for i in range(num):
                name = input("Enter Supervisor name: ")
                if not name.isalpha():
                    print("Invalid data format. Name should contain only alphabets. ")
                    return False
                email = input("Enter Supervisor email: ")
                if not InputValidations.validate_email(email):
                    return False

                sql = """INSERT INTO Supervisors (name, email,TeamName)
                           VALUES ('{}','{}','{}')""".format(name,email,team_name)

                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                print("Supervisor created successfully!\n")
            print("Team created successfully!")

        except Exception as e:
            print("Error is", e)
        finally:
            Admin.admin_supervisor_mgmnt(self)

    def get_supervisor_by_id(self, supervisor_id):

        """
        Get details of a particular supervisor.
        """
        sql = "SELECT name,email,assigned,TeamName FROM Supervisors WHERE id = {}".format(supervisor_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()

        if record:
            print("Name : {}".format(record[0]))
            print("Email : {}".format(record[1]))
            print("Assigned : {}".format(record[2]))
            print("Team Name : {}".format(record[3]))
            return record
        else:
            print("Invalid Id")
            return False

    def update_supervisor(self):
        """
        update details of a particular supervisor.
        :return:
        """
        try:
            supervisor_id = int(input("Enter Supervisor Id "))
            record = self.get_supervisor_by_id(supervisor_id)
            if record:
                name = (input("Enter Updated Name or Enter to continue ") or record[0])
                if not name.isalpha():
                    print("Invalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue ") or record[1])
                if not InputValidations.validate_email(email):
                    return False
                team_name = (input("Enter Updated Role or Enter to continue ") or record[3])

                sql = ''' UPDATE Supervisors
                                  SET name = '{}' ,
                                      email = '{}' ,
                                      TeamName = '{}'                      
                                  WHERE id = {}'''.format(name, email, team_name, supervisor_id)

                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                    self.conn.commit()

                print("Record Updated Successfully")
            record = self.get_supervisor_by_id(supervisor_id)

        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False
        finally:
            Admin.admin_supervisor_mgmnt(self)

    def delete_supervisor(self):
        """
        delete supervisor.
        :return:
        """
        try:
            Admin.show_allsupervisors(self)
            supervisor_id = int(input("Enter supervisor id: "))
            sql = 'DELETE FROM Supervisors WHERE id={}'.format(supervisor_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            print("Supervisor deleted successfully")
        except Exception as e:
            print("error", e)
        finally:
            Admin.admin_supervisor_mgmnt(self)

    def delete_supervisor_team(self):
        """
        delete entire supervision team.
        :return:
        """
        try:
            Admin.show_allsupervisors(self)
            team_name = input("Enter Team Name: ")
            sql = 'DELETE FROM Supervisors WHERE TeamName="{}"'.format(team_name)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            print("Supervision Team deleted successfully")
        except Exception as e:
            print("error", e)

        finally:
            Admin.admin_supervisor_mgmnt(self)

    def show_allsupervisors(self):
        """
        show details of all supervisors.
        :return:
        """
        try:
            sql = "select * from Supervisors order by TeamName"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("Supervisor id : {}".format(i[0]))
                print("Name : {}".format(i[1]))
                print("Email : {}".format(i[2]))
                print("Assigned : {}".format(i[4]))
                print("Team Name : {}".format(i[5]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")

    def assign_supervisor(self):
        """assign a supervision team to investigate the complaint"""
        try:
            Admin.show_complaints(self)
            c_id = int(input("Enter Complaint id: "))
            Admin.show_unassigned_supervisors(self)
            team_name = input("Enter name of the team you want to assign: ")

            sql = 'UPDATE Supervisors Set assigned = "yes" WHERE TeamName = "{}"'.format(team_name)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            sql1 = 'UPDATE Complaints Set status = "WIP",assigned_team = "{}" WHERE id = {}'.format(team_name,c_id)
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(sql1)
                self.conn.commit()
            print("Assigned Successfully!")

        except Exception as e:
            print('error', e)

        finally:
            Admin.admin_supervisor_mgmnt(self)

    def show_unassigned_supervisors(self):
        """
        show supervision teams that've not been assigned to any complaints.
        :return:
        """
        try:
            sql = "Select TeamName from Supervisors where assigned = 'no' group by TeamName"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("\n Unassigned Teams: ")
                print("Team : {}\n".format(i[0]))

        except Exception as e:
            print("Error in reading data")

    # SHOW COMPLAINTS
    def show_complaints(self):
        """
        show complaint details.
        :return:
        """
        try:
            sql = "Select * from Complaints where status = 'open' "
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("Complaint_id : {}".format(i[0]))
                print("Accident : {}".format(i[1]))
                print("Comments : {}".format(i[2]))
                print("----------------------------")



        except Exception as e:
            print("Error in reading data")

    def show_all_reports(self):
        """
        show details of all reports.
        :return:
        """
        try:
            sql = "Select r.id,r.complaint_id,r.TeamName,r.root_cause,r.details,r.no_of_people_affected,r.no_of_casualties,r.status,c.accident_name,c.comments from Report r join Complaints c on r.complaint_id = c.id"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)
            for i in result:
                print("Report Id : {}".format(i[0]))
                print("Complaint Id : {}".format(i[1]))
                print("Team Number : {}".format(i[2]))
                print("Root Cause : {}".format(i[3]))
                print("Details : {}".format(i[4]))
                print("Number of people affected : {}".format(i[5]))
                print("Number of Casualties : {}".format(i[6]))
                print("Status : {}".format(i[7]))
                print("Accident Name : {}".format(i[8]))
                print("Comments : {}".format(i[9]))
                print("----------------------------")


        except Exception as e:
            print("Error in reading data")
        finally:
            Admin.admin_report_management(self)

    def show_approved_reports(self):
        """
        show details of reports that've been approved.
        :return:
        """
        try:
            sql = "Select r.id,r.complaint_id,r.TeamName,r.root_cause,r.details,r.no_of_people_affected,r.no_of_casualties,c.accident_name,c.comments from Report r join Complaints c on r.complaint_id = c.id where r.status = 'approved'"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("Report Id : {}".format(i[0]))
                print("Complaint Id : {}".format(i[1]))
                print("Team Number : {}".format(i[2]))
                print("Root Cause : {}".format(i[3]))
                print("Details : {}".format(i[4]))
                print("Number of people affected : {}".format(i[5]))
                print("Number of Casualties : {}".format(i[6]))
                print("Accident Name : {}".format(i[7]))
                print("Comments : {}".format(i[8]))
                print("----------------------------")

        except Exception as e:
            print("Error in reading data")
        finally:
            Admin.admin_report_management(self)

    def show_rejected_reports(self):
        """
        show details of reports that've been rejected.
        :return:
        """
        try:
            sql = "Select r.id,r.complaint_id,r.TeamName,r.root_cause,r.details,r.no_of_people_affected,r.no_of_casualties,c.accident_name,c.comments from Report r join Complaints c on r.complaint_id = c.id where r.status = 'rejected'"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("Report Id : {}".format(i[0]))
                print("Complaint Id : {}".format(i[1]))
                print("Team Number : {}".format(i[2]))
                print("Root Cause : {}".format(i[3]))
                print("Details : {}".format(i[4]))
                print("Number of people affected : {}".format(i[5]))
                print("Number of Casualties : {}".format(i[6]))
                print("Accident Name : {}".format(i[7]))
                print("Comments : {}".format(i[8]))
                print("----------------------------")


        except Exception as e:
            print("Error in reading data")
        finally:
            Admin.admin_report_management(self)

    def show_pending_reports(self):
        """
        show details of reports that're pending approval and provide an option to approve/reject them.
        :return:
        """
        try:
            sql = "Select r.id,r.complaint_id,r.TeamName,r.root_cause,r.details,r.no_of_people_affected,r.no_of_casualties,r.status,c.accident_name,c.comments from Report r join Complaints c on r.complaint_id = c.id where r.status = 'none'"
            with self.conn:
                cur = self.conn.cursor()
                result = cur.execute(sql)

            for i in result:
                print("Report Id : {}".format(i[0]))
                print("Complaint Id : {}".format(i[1]))
                print("Team Number : {}".format(i[2]))
                print("Root Cause : {}".format(i[3]))
                print("Details : {}".format(i[4]))
                print("Number of people affected : {}".format(i[5]))
                print("Number of Casualties : {}".format(i[6]))
                print("Accident Name : {}".format(i[7]))
                print("Comments : {}".format(i[8]))
                print("----------------------------")

            r_id = int(input("Enter Report Id: "))
            val = input("Enter 'a' to Approve or 'r' to Reject or 'b' to go Back:   ")
            if val is 'a':
                sql = 'update Report set status = "approved" where id = {}'.format(r_id)
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                    self.conn.commit()
                print("Report approved successfully!")
                sql1 = 'select complaint_id from Report where id = {}'.format(r_id)
                with self.conn:
                    cur = self.conn.cursor()
                    res = cur.execute(sql1)
                for i in res:
                    Admin.c_id = i[0]
                sql2 = 'update Complaints set status = "closed" where id = {}'.format(Admin.c_id)
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql2)
                    self.conn.commit()
            elif val is 'r':
                sql = 'update Report set status = "rejected" where id = {}'.format(r_id)
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(sql)
                    self.conn.commit()
                print("Report Rejected successfully!")
            elif val is 'b':
                Admin.admin_report_management(self)
            else:
                print("Invalid Choice. Please try again!")
                Admin.show_pending_reports(self)

        except Exception as e:
            print("Error in reading data")
        finally:
            Admin.admin_report_management(self)

