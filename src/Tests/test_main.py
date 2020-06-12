import mock
from src.Main import login_menu


class TestMain:
    @mock.patch('src.EmployeeService.Employee.employee_tasks')
    @mock.patch('src.EmployeeService.Employee.employee_login')
    @mock.patch('src.EmployeeService.Employee')
    @mock.patch('src.AdminService.Admin.admin_tasks')
    @mock.patch('src.AdminService.Admin.admin_login')
    @mock.patch('src.AdminService.Admin')
    @mock.patch('src.Main.input')
    def test_login_menu(self, inputs, mock_admin, mock_admin_login,mock_admin_tasks, mock_employee, mock_employee_login,mock_employee_tasks):
        inputs.side_effect = ['1', '2', '4', '3']
        mock_admin.admin_login.return_value = True
        mock_employee.employee_login.return_value = True

        login_menu()

        mock_admin.admin_tasks.assert_called_once_with()
        mock_employee.employee_tasks.assert_called_once_with()
