from getpass import getpass
from src import InputValidations
from src.AdminRepository import AdminRepository
from src.InputValidations import validate_date
from src.Models import EmployeeModel, CabModel, RouteModel, CabRouteModel


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
        user = self.admin_repository.admin_login(email)
        if user:
            password = getpass('Enter Password: ')
            if user[1] == password:
                print("Authentication Successful")
                self.admin_id = user[2]
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
                self.get_all_cab_routes()
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
            employee = EmployeeModel(name=name, email=email)
            self.admin_repository.create_employee(employee)
            print("Employee created successfully!")
            return True
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def get_employee_by_id(self, employee_id):
        """
        Get details of a particular employee.
        """
        employee = self.admin_repository.get_employee_by_id(employee_id)
        if employee:
            print('''Name: {}\nEmail: {}\n
                      '''.format(employee[0], employee[1]))
            return employee
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
            employee = self.get_employee_by_id(employee_id)
            if employee:
                name = (input("Enter Updated Name or Enter to continue ") or employee[0])
                if not name.isalpha():
                    print("Invalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue ") or employee[1])
                if not InputValidations.validate_email(email):
                    return False
                self.admin_repository.update_employee(name, email, employee_id)
                print("Record Updated Successfully")
            updated_employee = self.get_employee_by_id(employee_id)
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
            employee = self.get_employee_by_id(employee_id)
            if employee:
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
            employees = self.admin_repository.show_all_employees()
            if employees:
                for employee in employees:
                    print("Employee Id : {}".format(employee[0]))
                    print("Name : {}".format(employee[1]))
                    print("Email : {}".format(employee[2]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def create_cab(self):
        """
        create a new cab.
        :return:
        """
        try:
            cab_number = input("Enter Cab Number: ")
            capacity = int(input("Enter seating capacity: "))
            cab = CabModel(cab_number=cab_number, capacity=capacity)
            self.admin_repository.create_cab(cab)
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
            route = RouteModel(route=route)
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
        cab = self.admin_repository.get_cab_by_id(cab_num)
        if cab:
            print('''Cab Number: {}\nSeating Capacity: {}\n
                      '''.format(cab[0], cab[1]))
            return cab
        else:
            print("Invalid Cab Number")
            return False

    def get_route_by_id(self, route_id):
        """
        Get details of a particular route.
        """
        route = self.admin_repository.get_route_by_id(route_id)
        if route:
            print('''Route Id: {}\nRoute: {}\n
                      '''.format(route[0], route[1]))
            return route
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
            cab = self.get_cab_by_id(cab_num)
            if cab:
                capacity = (int(input("Enter Updated Seating Capacity or Enter to continue ")) or cab[1])
                self.admin_repository.update_cab(capacity, cab_num)
                print("Record Updated Successfully")
            updated_cab = self.get_cab_by_id(cab_num)
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
            cab = self.get_cab_by_id(cab_num)
            if cab:
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
            route = self.get_route_by_id(route_id)
            if route:
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
            cabs = self.admin_repository.show_all_cabs()

            if cabs:
                for cab in cabs:
                    print("Cab Number: {}".format(cab[0]))
                    print("Seating Capacity : {}".format(cab[1]))
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
            routes = self.admin_repository.show_all_routes()
            if routes:
                for route in routes:
                    print("Route Id: {}".format(route[0]))
                    print("Route : {}".format(route[1]))
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
                cab_route = CabRouteModel(cab_number=cab_num, route_id=route_id, stop_name=stop_name,
                                          stop_stage=stop_stage, timings=timings)
                self.admin_repository.create_cab_route(cab_route)
                print("stop added successfully!\n")
            print("Route added successfully!")
            return True
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def get_cab_route_by_cab_num(self, cab_num):
        """
        Get route details of a particular cab.
        """
        try:
            cab_routes = self.admin_repository.get_cab_route_by_cab_num(cab_num)
            if cab_routes:
                for cab_route in cab_routes:
                    print("\nId : {}".format(cab_route[0]))
                    print("Cab Number : {}".format(cab_route[1]))
                    print("Route Id : {}".format(cab_route[2]))
                    print("Stop Name : {}".format(cab_route[3]))
                    print("Stop stage : {}".format(cab_route[4]))
                    print("Timings : {}".format(cab_route[5]))
                    print("----------------------------")
                return True
            else:
                print("Invalid Input")
                return False
        except Exception as e:
            print("Some Error occurred. Please try again.")
            return False

    def get_all_cab_routes(self):
        """
        Get route details of cabs.
        """
        try:
            cab_routes = self.admin_repository.get_all_cab_routes()
            if cab_routes:
                for cab_route in cab_routes:
                    print("\nId : {}".format(cab_route[0]))
                    print("Cab Number : {}".format(cab_route[1]))
                    print("Route Id : {}".format(cab_route[2]))
                    print("Stop Name : {}".format(cab_route[3]))
                    print("Stop stage : {}".format(cab_route[4]))
                    print("Timings : {}".format(cab_route[5]))
                    print("----------------------------")
                return True
            else:
                print("Data Empty/Not Found.")
                return False
        except Exception as e:
            print("Some error occurred. Please try again.")
            return False

    def get_cab_route_by_id(self, id):
        """
        Get stop details of a particular cab.
        """
        try:
            cab_route = self.admin_repository.get_cab_route_by_id(id)
            if cab_route:
                print("Cab Number : {}".format(cab_route[1]))
                print("Route Id : {}".format(cab_route[2]))
                print("Stop Name : {}".format(cab_route[3]))
                print("Stop stage : {}".format(cab_route[4]))
                print("Timings : {}".format(cab_route[5]))
                return cab_route
            else:
                print("Invalid Input")
                return False
        except Exception as e:
            print("Some Error occurred. Please try again.")
            return False

    def update_cab_route(self):
        """
        update route details of a particular cab.
        :return:
        """
        try:
            cab_num = input("Enter Cab Number: ")
            cab_routes = self.get_cab_route_by_cab_num(cab_num)
            if cab_routes:
                id = int(input("Enter Id of the record you want to update: "))
                cab_route = self.get_cab_route_by_id(id)
                if cab_route:
                    updated_cab_num = (input("Enter Updated Cab Number or Enter to continue ") or cab_route[1])
                    route_id = (input("Enter Updated Route Id or Enter to continue ") or cab_route[2])
                    stop_name = (input("Enter Updated stop name or Enter to continue ") or cab_route[3])
                    stop_stage = (input("Enter Updated stage or Enter to continue ") or cab_route[4])
                    timings = (input("Enter Updated timings or Enter to continue ") or cab_route[5])
                    self.admin_repository.update_cab_route(updated_cab_num, route_id, stop_name, stop_stage, timings,
                                                           id)
                    print("\nRecord Updated Successfully")
                    updated_cab_route = self.get_cab_route_by_id(id)
                    return True
                else:
                    print("Invalid input.")
                    return False
            else:
                print("Record not found.")
                return False
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
            cab_routes = self.get_cab_route_by_cab_num(cab_num)
            if cab_routes:
                cab_route_id = input("Enter Cab Route Id: ")
                self.admin_repository.delete_cab_route(cab_num, cab_route_id)
                print("Deleted successfully.")
                return True
            else:
                print("Invalid input.")
                return False

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
            bookings = self.admin_repository.show_emp_bookings(emp_id)
            if bookings:
                for booking in bookings:
                    print("Booking Id : {}".format(booking[5]))
                    print("Date : {}".format(booking[0]))
                    print("Pick up time : {}".format(booking[1]))
                    print("Cab_Number : {}".format(booking[2]))
                    print("Pick up location: {}".format(booking[3]))
                    print("Destination : {}".format(booking[4]))
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
            bookings = self.admin_repository.show_total_bookings_day(booking_date)
            if bookings:
                print("Date: {}".format(bookings[0]))
                print("Total Bookings : {}".format(bookings[1]))
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
            bookings = self.admin_repository.show_total_bookings_week(booking_week)
            if bookings:
                print("Date: {}".format(bookings[0]))
                print("Total Bookings : {}".format(bookings[1]))
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
            bookings = self.admin_repository.show_total_bookings_month(booking_month)
            if bookings:
                print("Date: {}".format(bookings[0]))
                print("Total Bookings : {}".format(bookings[1]))
                return True
            else:
                print("No records found.")
                return False
        except Exception as e:
            print("Some Error occurred. Please try again.")
            return False
