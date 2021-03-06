from datetime import datetime, timedelta

import mock
from src import AdminService


class TestAdminService:
    @mock.patch('src.AdminService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_login_password_match(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1)
        test_class = AdminService.Admin()

        result = test_class.admin_login()

        assert result is True

    @mock.patch('src.AdminService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_login_password_mismatch(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1)
        test_class = AdminService.Admin()

        result = test_class.admin_login()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_login_invalid_user(self, inputs, mock_conn):
        inputs.return_value = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = None
        test_class = AdminService.Admin()

        result = test_class.admin_login()

        assert result is False

    @mock.patch('src.AdminService.Admin.admin_employee_mgmnt')
    @mock.patch('src.AdminService.Admin.admin_cab_mgmnt')
    @mock.patch('src.AdminService.Admin.admin_route_management')
    @mock.patch('src.AdminService.Admin.admin_booking_management')
    @mock.patch('src.AdminService.input')
    def test_admin_tasks(self, inputs, mock_admin_employee_mgmnt, mock_admin_cab_mgmnt, mock_admin_route_management,
                         mock_admin_booking_management):
        inputs.side_effect = ['1', '2', '3', '4', '6', '5']
        test_class = AdminService.Admin()

        test_class.admin_tasks()

        mock_admin_employee_mgmnt.assert_called_once_with()
        mock_admin_cab_mgmnt.assert_called_once_with()
        mock_admin_route_management.assert_called_once_with()
        mock_admin_booking_management.assert_called_once_with()

    @mock.patch('src.AdminService.Admin.create_employee')
    @mock.patch('src.AdminService.Admin.show_allemployees')
    @mock.patch('src.AdminService.Admin.update_employee')
    @mock.patch('src.AdminService.Admin.delete_employee')
    @mock.patch('src.AdminService.input')
    def test_admin_employee_mgmnt(self, inputs, mock_create_employee, mock_show_allemployees, mock_update_employee,
                                  mock_delete_employee):
        inputs.side_effect = ['1', '2', '3', '4', '6', '5']
        test_class = AdminService.Admin()

        test_class.admin_employee_management()

        mock_create_employee.assert_called_once_with()
        mock_show_allemployees.assert_called_once_with()
        mock_update_employee.assert_called_once_with()
        mock_delete_employee.assert_called_once_with()

    @mock.patch('src.AdminService.Admin.create_cab')
    @mock.patch('src.AdminService.Admin.update_cab')
    @mock.patch('src.AdminService.Admin.delete_cab')
    @mock.patch('src.AdminService.Admin.show_all_cabs')
    @mock.patch('src.AdminService.input')
    def test_admin_cab_mgmnt(self, inputs, mock_create_cab, mock_update_cab, mock_delete_cab,
                             mock_show_all_cabs):
        inputs.side_effect = ['1', '2', '3', '4', '6', '5']
        test_class = AdminService.Admin()

        test_class.admin_cab_management()

        mock_create_cab.assert_called_once_with()
        mock_update_cab.assert_called_once_with()
        mock_delete_cab.assert_called_once_with()
        mock_show_all_cabs.assert_called_once_with()

    @mock.patch('src.AdminService.Admin.create_route')
    @mock.patch('src.AdminService.Admin.delete_route')
    @mock.patch('src.AdminService.Admin.show_all_routes')
    @mock.patch('src.AdminService.Admin.create_cab_route')
    @mock.patch('src.AdminService.Admin.update_cab_route')
    @mock.patch('src.AdminService.Admin.get_all_routes')
    @mock.patch('src.AdminService.Admin.delete_cab_route')
    @mock.patch('src.AdminService.input')
    def test_admin_route_management(self, inputs, mock_create_route, mock_delete_route, mock_show_all_routes,
                                    mock_create_cab_route, mock_update_cab_route, mock_get_all_routes,
                                    mock_delete_cab_route):
        inputs.side_effect = ['1', '2', '3', '4', '5', '6', '7', '9', '8']
        test_class = AdminService.Admin()

        test_class.admin_route_management()

        mock_create_route.assert_called_once_with()
        mock_delete_route.assert_called_once_with()
        mock_show_all_routes.assert_called_once_with()
        mock_create_cab_route.assert_called_once_with()
        mock_update_cab_route.assert_called_once_with()
        mock_get_all_routes.assert_called_once_with()
        mock_delete_cab_route.assert_called_once_with()

    @mock.patch('src.AdminService.Admin.show_emp_bookings')
    @mock.patch('src.AdminService.Admin.show_total_bookings_day')
    @mock.patch('src.AdminService.Admin.show_total_bookings_week')
    @mock.patch('src.AdminService.Admin.show_total_bookings_month')
    @mock.patch('src.AdminService.input')
    def test_admin_booking_management(self, inputs, mock_show_emp_bookings, mock_show_total_bookings_day,
                                      mock_show_total_bookings_week,
                                      show_total_bookings_month):
        inputs.side_effect = ['1', '2', '3', '4', '6', '5']
        test_class = AdminService.Admin()

        test_class.admin_booking_management()

        mock_show_emp_bookings.assert_called_once_with()
        mock_show_total_bookings_day.assert_called_once_with()
        mock_show_total_bookings_week.assert_called_once_with()
        show_total_bookings_month.assert_called_once_with()

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_create_employee(self, inputs, mock_conn):
        inputs.side_effect = ['test', 'test@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.create_employee()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_create_employee_invalid_name(self, inputs, mock_conn):
        inputs.side_effect = ['test12', 'test@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.create_employee()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_create_employee_invalid_email(self, inputs, mock_conn):
        inputs.side_effect = ['test', 'testgmail']

        test_class = AdminService.Admin()

        result = test_class.create_employee()

        assert result is False

    def test_create_employee_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.create_employee()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_get_employee_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ['Name', 'email@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.get_employee_by_id(1)

        assert result == ['Name', 'email@gmail.com']

    @mock.patch('src.Main.create_connection')
    def test_get_employee_by_id_invalid_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []

        test_class = AdminService.Admin()

        result = test_class.get_employee_by_id(1)

        assert result is False

    @mock.patch('src.AdminService.Admin.get_employee_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_update_employee(self, inputs, mock_conn, mock_get_employee_by_id):
        inputs.side_effect = [1, 'test', 'test@gmail.com']

        mock_get_employee_by_id.return_value = ['Name', 'email@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.update_employee()

        assert result is True

    @mock.patch('src.AdminService.Admin.get_employee_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_update_employee_invalid_name(self, inputs, mock_conn, mock_get_employee_by_id):
        inputs.side_effect = [1, 'test12', 'test@gmail.com']

        mock_get_employee_by_id.return_value = ['Name', 'email@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.update_employee()

        assert result is False

    @mock.patch('src.AdminService.Admin.get_employee_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_update_employee_invalid_email(self, inputs, mock_conn, mock_get_employee_by_id):
        inputs.side_effect = [1, 'test', 'testgmail.com']

        mock_get_employee_by_id.return_value = ['Name', 'email@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.update_employee()

        assert result is False

    def test_update_employee_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.update_employee()

        assert result is False

    @mock.patch('src.AdminService.Admin.show_allemployees')
    @mock.patch('src.AdminService.Admin.get_employee_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_employee(self, inputs, mock_conn, mock_get_employee_by_id, mock_show_allemployees):
        inputs.side_effect = [1]

        mock_get_employee_by_id.return_value = ['Name', 'email@gmail.com']

        test_class = AdminService.Admin()

        result = test_class.delete_employee()

        mock_show_allemployees.assert_called_once_with()
        assert result is True

    @mock.patch('src.AdminService.Admin.show_allemployees')
    @mock.patch('src.AdminService.Admin.get_employee_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_employee_invalid_id(self, inputs, mock_conn, mock_get_employee_by_id, mock_show_allemployees):
        inputs.side_effect = [1]

        mock_get_employee_by_id.return_value = []

        test_class = AdminService.Admin()

        result = test_class.delete_employee()

        mock_show_allemployees.assert_called_once_with()
        assert result is False

    @mock.patch('src.AdminService.Admin.show_allemployees')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_employee_unknown_error(self, inputs, mock_conn, mock_show_allemployees):
        inputs.side_effect = ['a']

        test_class = AdminService.Admin()

        result = test_class.delete_employee()

        mock_show_allemployees.assert_called_once_with()
        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_allemployees(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(1, 'test', 'email@gmail.com')]

        test_class = AdminService.Admin()

        result = test_class.show_all_employees()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_allemployees_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_all_employees()

        assert result is False

    # ---------------------------------------------------------

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_create_cab(self, inputs, mock_conn):
        inputs.side_effect = ['cab123', 1]

        test_class = AdminService.Admin()

        result = test_class.create_cab()

        assert result is True

    @mock.patch('src.AdminService.input')
    def test_create_cab_unknown_error(self, inputs):
        inputs.side_effect = ['cab123', 'b']

        test_class = AdminService.Admin()

        result = test_class.create_cab()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_create_route(self, inputs, mock_conn):
        inputs.side_effect = ['cab123']

        test_class = AdminService.Admin()

        result = test_class.create_route()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_create_route_unknown_error(self, mock_conn):
        test_class = AdminService.Admin()

        result = test_class.create_route()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_get_cab_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ['cab123', 2]

        test_class = AdminService.Admin()

        result = test_class.get_cab_by_id('test')

        assert result == ['cab123', 2]

    @mock.patch('src.Main.create_connection')
    def test_get_cab_by_id_invalid_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []

        test_class = AdminService.Admin()

        result = test_class.get_cab_by_id('test')

        assert result is False

    def test_get_cab_by_id_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.get_cab_by_id('test')

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_get_route_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = [1, 'route123']

        test_class = AdminService.Admin()

        result = test_class.get_route_by_id(1)

        assert result == [1, 'route123']

    @mock.patch('src.Main.create_connection')
    def test_get_route_by_id_invalid_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []

        test_class = AdminService.Admin()

        result = test_class.get_route_by_id(1)

        assert result is False

    @mock.patch('src.AdminService.Admin.get_cab_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_update_cab(self, inputs, mock_conn, mock_get_cab_by_id):
        inputs.side_effect = ['cab123', 1]

        mock_get_cab_by_id.return_value = ['cab123', 2]

        test_class = AdminService.Admin()

        result = test_class.update_cab()

        assert result is True

    @mock.patch('src.AdminService.Admin.get_cab_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_update_cab_value_error(self, inputs, mock_conn, mock_get_cab_by_id):
        inputs.side_effect = ['cab123', 'a']

        mock_get_cab_by_id.return_value = ['cab123', 2]

        test_class = AdminService.Admin()

        result = test_class.update_cab()

        assert result is False

    def test_update_cab_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.update_cab()

        assert result is False

    @mock.patch('src.AdminService.Admin.show_all_cabs')
    @mock.patch('src.AdminService.Admin.get_cab_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_cab(self, inputs, mock_conn, mock_get_cab_by_id, mock_show_all_cabs):
        inputs.side_effect = ['1']

        mock_get_cab_by_id.return_value = ['cab123', 2]
        test_class = AdminService.Admin()

        result = test_class.delete_cab()

        mock_show_all_cabs.assert_called_once_with()
        assert result is True

    @mock.patch('src.AdminService.Admin.show_all_cabs')
    @mock.patch('src.AdminService.Admin.get_cab_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_cab_invalid_id(self, inputs, mock_conn, mock_get_cab_by_id, mock_show_all_cabs):
        inputs.side_effect = ['1']

        mock_get_cab_by_id.return_value = []
        test_class = AdminService.Admin()

        result = test_class.delete_cab()

        mock_show_all_cabs.assert_called_once_with()
        assert result is False

    def test_delete_cab_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.delete_cab()

        assert result is False

    @mock.patch('src.AdminService.Admin.show_all_routes')
    @mock.patch('src.AdminService.Admin.get_route_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_cab(self, inputs, mock_conn, mock_get_route_by_id, mock_show_all_routes):
        inputs.side_effect = ['1']

        mock_get_route_by_id.return_value = [1, 'r123']
        test_class = AdminService.Admin()

        result = test_class.delete_route()

        mock_show_all_routes.assert_called_once_with()
        assert result is True

    @mock.patch('src.AdminService.Admin.show_all_routes')
    @mock.patch('src.AdminService.Admin.get_route_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_delete_cab_invalid_id(self, inputs, mock_conn, mock_get_route_by_id, mock_show_all_routes):
        inputs.side_effect = ['1']

        mock_get_route_by_id.return_value = []
        test_class = AdminService.Admin()

        result = test_class.delete_route()

        mock_show_all_routes.assert_called_once_with()
        assert result is False

    def test_delete_route_unknown_error(self):
        test_class = AdminService.Admin()

        result = test_class.delete_route()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_all_cabs(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('cab123', 1)]

        test_class = AdminService.Admin()

        result = test_class.show_all_cabs()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_all_cabs_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_all_cabs()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_all_routes(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(1, 'r123')]

        test_class = AdminService.Admin()

        result = test_class.show_all_routes()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_all_routes_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_all_routes()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_emp_bookings(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [
            (1, '2020-01-01', '12:00', 'cab123', 's', 'd')]

        test_class = AdminService.Admin()

        result = test_class.show_emp_bookings()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_emp_bookings_invalid_id(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_emp_bookings()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_emp_bookings_unknown_error(self, inputs, mock_conn):
        inputs.side_effect = ['b']
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_emp_bookings()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_day(self, inputs, mock_conn):
        inputs.side_effect = ['2020-01-02']
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ['2020-01-02', 2]

        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_day()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_day_empty(self, inputs, mock_conn):
        inputs.side_effect = ['a']
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_day()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_day_unknown_error(self, inputs, mock_conn):
        inputs.side_effect = ['b']
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_day()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_week(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ['01', 2]

        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_week()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_week_empty(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_week()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_week_unknown_error(self, inputs, mock_conn):
        inputs.side_effect = ['b']
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_week()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_month(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ['01', 2]

        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_month()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_month_empty(self, inputs, mock_conn):
        inputs.side_effect = [1]
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_month()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_show_total_bookings_month_unknown_error(self, inputs, mock_conn):
        inputs.side_effect = ['b']
        mock_conn.return_value.cursor.return_value.fetchone.return_value = []
        test_class = AdminService.Admin()

        result = test_class.show_total_bookings_month()

        assert result is False
