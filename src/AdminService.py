from getpass import getpass
from src import InputValidations
from src.AdminRepository import AdminRepository
from src.InputValidations import validate_date


class Admin:

    def __init__(self):
        self.admin_id = None
        self.admin_repository = AdminRepository()

    def admin_login(self):
        """
        admin authentication
        :return:
        """
        email = input("Enter Email: ")

        record = self.admin_repository.admin_login(email)
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
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Employee Management\n"
                  "2: Cab Management\n"
                  "3: Route Management\n"
                  "4: Bookings\n"
                  "5: Exit\n")
            option = input("Select option: ")

            if option == '1':
                self.admin_employee_management()
            elif option == '2':
                self.admin_cab_management()
            elif option == '3':
                self.admin_route_management()
            elif option == '4':
                self.admin_booking_management()
            elif option == '5':
                print("Thank You")
            else:
                print("Invalid choice")

    def admin_employee_management(self):
        """
        employee management.
        :return:
        """
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Create Employee Profile\n"
                  "2: Show All Employees\n"
                  "3: Update Employee Profile\n"
                  "4: Delete Employee Profile\n"
                  "5: Go back\n")
            option = input("Select option: ")
            if option == '1':
                self.create_employee()
            elif option == '2':
                self.show_all_employees()
            elif option == '3':
                self.update_employee()
            elif option == '4':
                self.delete_employee()
            elif option == '5':
                print("")
            else:
                print("Invalid choice")

    def admin_cab_management(self):
        """
        cab management.
        :return:
        """
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Add New Cab \n"
                  "2: Update Cab \n"
                  "3: Delete Cab \n"
                  "4: Show All Cabs \n"
                  "5: Back \n")
            option = input("Select task: ")
            if option == '1':
                self.create_cab()
            elif option == '2':
                self.update_cab()
            elif option == '3':
                self.delete_cab()
            elif option == '4':
                self.show_all_cabs()
            elif option == '5':
                print("")
            else:
                print("Invalid choice.")

    def admin_route_management(self):
        """
        route management.
        :return:
        """
        option = ''
        while option != '8':
            print("\nMenu\n"
                  "1: Create route\n"
                  "2: Delete route\n"
                  "3: Show all routes\n"
                  "4: Add new cab to route\n"
                  "5: Update Cab route\n"
                  "6: Show all routes of a cab\n"
                  "7: Delete cab route\n"
                  "8: Go back\n")
            option = input("Select task: ")
            if option == '1':
                self.create_route()
            elif option == '2':
                self.delete_route()
            elif option == '3':
                self.show_all_routes()
            elif option == '4':
                self.create_cab_route()
            elif option == '5':
                self.update_cab_route()
            elif option == '6':
                self.get_all_routes()
            elif option == '7':
                self.delete_cab_route()
            elif option == '8':
                print("")
            else:
                print("Invalid choice.")

    def admin_booking_management(self):
        """
        booking management.
        :return:
        """
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Show bookings of an employee\n"
                  "2: Show Total bookings for a day\n"
                  "3: Show Total bookings for a week\n"
                  "4: Show Total bookings for a month\n"
                  "5: Go back\n")
            option = input("Select task: ")
            if option == '1':
                self.show_emp_bookings()
            elif option == '2':
                self.show_total_bookings_day()
            elif option == '3':
                self.show_total_bookings_week()
            elif option == '4':
                self.show_total_bookings_month()
            elif option == '5':
                print("")
            else:
                print("Invalid choice.")

    def create_employee(self):
        """
        create a new employee.
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

            self.admin_repository.create_employee(name, email)
            print("Employee created successfully!")
            return True

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def get_employee_by_id(self, employee_id):
        """
        Get details of a particular employee.
        """

        record = self.admin_repository.get_employee_by_id(employee_id)

        if record:
            print('''Name: {}\nEmail: {}\n
                      '''.format(record[0], record[1]))
            return record
        else:
            print("Invalid Id")
            return False

    def update_employee(self):
        """
        update employee details.
        :return:
        """
        try:
            employee_id = int(input("Enter Employee Id "))
            record = self.get_employee_by_id(employee_id)
            if record:
                name = (input("Enter Updated Name or Enter to continue ") or record[0])
                if not name.isalpha():
                    print("Invalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue ") or record[1])
                if not InputValidations.validate_email(email):
                    return False
                self.admin_repository.update_employee(name, email, employee_id)
                print("Record Updated Successfully")
            record = self.get_employee_by_id(employee_id)
            return True
        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_employee(self):
        """
        delete employee.
        :return:
        """
        try:
            self.show_all_employees()
            employee_id = int(input("Enter the Employee id: "))
            result = self.get_employee_by_id(employee_id)
            if result:
                self.admin_repository.delete_employee(employee_id)
                print("Employee deleted successfully")
                return True
            else:
                print("Invalid employee Id.")
                return False
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def show_all_employees(self):
        """
        show details of all employees.
        :return:
        """
        try:
            result = self.admin_repository.show_all_employees()

            if result:
                for i in result:
                    print("Employee Id : {}".format(i[0]))
                    print("Name : {}".format(i[1]))
                    print("Email : {}".format(i[2]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    # ----------------------------------------------------------

    def create_cab(self):
        """
        create a new cab.
        :return:
        """
        try:
            cab_num = input("Enter Cab Number: ")
            capacity = int(input("Enter seating capacity: "))
            self.admin_repository.create_cab(cab_num, capacity)
            print("Cab added successfully!")
            return True

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def create_route(self):
        """
        create a new route.
        :return:
        """
        try:
            route = input("Enter Route/Route Description: ")
            self.admin_repository.create_route(route)
            print("Route added successfully!")
            return True

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def get_cab_by_id(self, cab_num):
        """
        Get details of a particular cab.
        """
        record = self.admin_repository.get_cab_by_id(cab_num)

        if record:
            print('''Cab Number: {}\nSeating Capacity: {}\n
                      '''.format(record[0], record[1]))
            return record
        else:
            print("Invalid Cab Number")
            return False

    def get_route_by_id(self, route_id):
        """
        Get details of a particular route.
        """
        record = self.admin_repository.get_route_by_id(route_id)

        if record:
            print(record)
            print('''Route Id: {}\nRoute: {}\n
                      '''.format(record[0], record[1]))
            return record
        else:
            print("Invalid Route Id")
            return False

    def update_cab(self):
        """
        update cab details.
        :return:
        """
        try:
            cab_num = input("Enter Cab Number: ")
            record = self.get_cab_by_id(cab_num)
            if record:
                capacity = (int(input("Enter Updated Seating Capacity or Enter to continue ")) or record[1])
                self.admin_repository.update_cab(capacity, cab_num)
                print("Record Updated Successfully")
            record = self.get_cab_by_id(cab_num)
            return True
        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_cab(self):
        """
        delete cab.
        :return:
        """
        try:
            self.show_all_cabs()
            cab_num = input("Enter the Cab Number: ")
            result = self.get_cab_by_id(cab_num)
            if result:
                self.admin_repository.delete_cab(cab_num)
                print("Cab removed successfully")
                return True
            else:
                print("Invalid Cab Number.")
                return False
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def delete_route(self):
        """
        delete route.
        :return:
        """
        try:
            self.show_all_routes()
            route_id = int(input("Enter Route Id: "))
            result = self.get_route_by_id(route_id)
            if result:
                self.admin_repository.delete_route(route_id)
                print("Route removed successfully")
                return True
            else:
                print("Invalid Route Id.")
                return False
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def show_all_cabs(self):
        """
        show details of all cabs.
        :return:
        """
        try:
            result = self.admin_repository.show_all_cabs()

            if result:
                for i in result:
                    print("Cab Number: {}".format(i[0]))
                    print("Seating Capacity : {}".format(i[1]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def show_all_routes(self):
        """
        show details of all routes.
        :return:
        """
        try:
            result = self.admin_repository.show_all_routes()

            if result:
                for i in result:
                    print("Route Id: {}".format(i[0]))
                    print("Route : {}".format(i[1]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def create_cab_route(self):
        """
        add new route to cab.
        :return:
        """
        try:

            cab_num = input("Enter Cab Number: ")
            route_id = input("Enter Route Id: ")
            timings = input("Enter Timings in HH:MM format: ")

            num = int(input("Enter number of stops: "))
            for i in range(num):
                stop_name = input("Enter stop name: ")
                stop_stage = int(input("Enter stop stage (ex: In the route koramangala-hsr-btm, stage of btm is 2): "))
                self.admin_repository.create_cab_route(cab_num, route_id, stop_name, stop_stage, timings)

                print("stop added successfully!\n")
            print("Route added successfully!")
            return True

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def get_route_by_cab_num(self, cab_num):

        """
        Get route details of a particular cab.
        """
        record = self.admin_repository.get_route_by_cab_num(cab_num)

        if record:
            for i in record:
                print("\nId : {}".format(i[0]))
                print("Cab Number : {}".format(i[1]))
                print("Route Id : {}".format(i[2]))
                print("Stop Name : {}".format(i[3]))
                print("Stop stage : {}".format(i[4]))
                print("Timings : {}".format(i[5]))
                print("----------------------------")
            return True
        else:
            print("Invalid Input")
            return False

    def get_all_routes(self):
        """
        Get route details of cabs.
        """
        record = self.admin_repository.get_all_routes()

        if record:
            for i in record:
                print("\nId : {}".format(i[0]))
                print("Cab Number : {}".format(i[1]))
                print("Route Id : {}".format(i[2]))
                print("Stop Name : {}".format(i[3]))
                print("Stop stage : {}".format(i[4]))
                print("Timings : {}".format(i[5]))
                print("----------------------------")
            return True
        else:
            print("Data Empty/Not Found.")
            return False

    def get_cab_route_by_id(self, id):

        """
        Get stop details of a particular cab.
        """
        record = self.admin_repository.get_cab_route_by_id(id)


        if record:
            print("Cab Number : {}".format(record[1]))
            print("Route Id : {}".format(record[2]))
            print("Stop Name : {}".format(record[3]))
            print("Stop stage : {}".format(record[4]))
            print("Timings : {}".format(record[5]))
            return record
        else:
            print("Invalid Input")
            return False

    def update_cab_route(self):
        """
        update route details of a particular cab.
        :return:
        """
        try:
            cab_num = input("Enter Cab Number: ")
            records = self.get_route_by_cab_num(cab_num)
            if records:
                id = int(input("Enter Id of the record you want to update: "))
                record = self.get_cab_route_by_id(id)
                print(record)
                if record:
                    updated_cab_num = (input("Enter Updated Cab Number or Enter to continue ") or record[1])
                    route_id = (input("Enter Updated Route Id or Enter to continue ") or record[2])
                    stop_name = (input("Enter Updated stop name or Enter to continue ") or record[3])
                    stop_stage = (input("Enter Updated stage or Enter to continue ") or record[4])
                    timings = (input("Enter Updated timings or Enter to continue ") or record[5])
                    self.admin_repository.update_cab_route(updated_cab_num, route_id, stop_name, stop_stage, timings,
                                                              id)
                    print("\nRecord Updated Successfully")
                else:
                    print("Invalid input.")
            else:
                print("Record not found.")
                return False
            record = self.get_cab_route_by_id(id)
            return True

        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_cab_route(self):
        """
        delete cab route.
        :return:
        """
        try:
            cab_num = input("Enter Cab Number: ")
            records = self.get_route_by_cab_num(cab_num)
            if records:
                route_id = input("Enter Route Id: ")
                self.admin_repository.delete_cab_route(cab_num, route_id)
                print("Deleted successfully.")
                return True
            else:
                print("Invalid input.")

        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def show_emp_bookings(self):
        """
        show booking details of an employee.
        :return:
        """
        try:
            emp_id = int(input("Enter Employee Id: "))
            result = self.admin_repository.show_emp_bookings(emp_id)

            if result:
                for i in result:
                    print("Booking Id : {}".format(i[5]))
                    print("Date : {}".format(i[0]))
                    print("Pick up time : {}".format(i[1]))
                    print("Cab_Number : {}".format(i[2]))
                    print("Pick up location: {}".format(i[3]))
                    print("Destination : {}".format(i[4]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.")
            return False

    def show_total_bookings_day(self):
        """
        show total booking per day.
        :return:
        """
        try:
            booking_date = input("Enter Date in YYYY-MM-DD format: ")
            if not validate_date(booking_date):
                return False
            result = self.admin_repository.show_total_bookings_day(booking_date)

            if result:
                print("Date: {}".format(result[0]))
                print("Total Bookings : {}".format(result[1]))
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.")
            return False

    def show_total_bookings_week(self):
        """
        show total booking per week.
        :return:
        """
        try:
            week = int(input("Enter Week Number: "))
            booking_week = '%02d' % week
            result = self.admin_repository.show_total_bookings_week(booking_week)

            if result:
                print("Date: {}".format(result[0]))
                print("Total Bookings : {}".format(result[1]))
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.")
            return False

    def show_total_bookings_month(self):
        """
        show total booking per month.
        :return:
        """
        try:
            month = int(input("Enter Month:  "))
            booking_month = '%02d' % month
            result = self.admin_repository.show_total_bookings_month(booking_month)

            if result:
                print("Date: {}".format(result[0]))
                print("Total Bookings : {}".format(result[1]))
                return True
            else:
                print("No records found.")
                return False

        except Exception as e:
            print("Some Error occurred.")
            return False