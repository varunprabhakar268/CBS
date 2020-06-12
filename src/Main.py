from src import EmployeeService, AdminService


def login_menu():
    option = ''
    while option != '3':
        print("MAIN MENU")
        print("1. Admin Login")
        print("2. Employee Login")
        print("3. Exit")
        option = input("Select Your Option ")
        if option == '1':
            admin = AdminService.Admin()
            if admin.admin_login():
                admin.admin_tasks()
        elif option == '2':
            employee = EmployeeService.Employee()
            if employee.employee_login():
                employee.employee_tasks()
        elif option == '3':
            print("Thank You.")
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    login_menu()
