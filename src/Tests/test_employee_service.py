import mock
from src import EmployeeService


class TestEmployeeService:

    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_login_password_match(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is True

    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_login_password_mismatch(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is False

    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_login_first_time(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', None, 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_login_invalid_user(self, inputs, mock_conn):
        inputs.return_value = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = None
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_past_bookings(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [
            ('2020-05-28', '21:00', 'test', 'source', 'destination', 1)]

        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_past_bookings_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is False

    def test_show_past_bookings_unknown_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_upcoming_bookings(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [
            ('2020-05-28', '21:00', 'test', 'source', 'destination', 1)]

        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_upcoming_bookings_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is False

    def test_show_upcoming_bookings_unknown_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_all_routes(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(1, 'test')]

        test_class = EmployeeService.Employee()

        result = test_class.show_all_routes()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_all_routes_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_all_routes()

        assert result is False



    @mock.patch('src.Main.create_connection')
    def test_check_availability(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('cab123', '12:00:00', 2, 'stop', 2)]

        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_check_availability_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is False

    def test_check_availability_unknown_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_get_booking_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = [
            ('2020-01-01', '12:00:00', 'cab123', 1, 'source', 'destination')]

        test_class = EmployeeService.Employee()

        result = test_class.get_booking_by_id(1)

        assert result == [('2020-01-01', '12:00:00', 'cab123', 1, 'source', 'destination')]

    def test_get_booking_by_id_unknown_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.get_booking_by_id('a')

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_decrement_seats(self, mock_conn):
        test_class = EmployeeService.Employee()

        result = test_class.decrement_seats('cab123',1,'s','d','12:00')

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_increment_seats(self, mock_conn):
        test_class = EmployeeService.Employee()

        result = test_class.increment_seats('cab123',1,'s','d','12:00')

        assert result is True

    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    @mock.patch('src.EmployeeService.Employee.check_availability')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_book_cab(self,inputs, mock_conn,mock_show_all_routes,mock_check_availability):
        inputs.side_effect = ['1', 's', 'd', '12:00', 'cab', '13:00']

        mock_show_all_routes.return_value = True
        mock_check_availability.return_value = True

        test_class = EmployeeService.Employee()

        result = test_class.book_cab()

        assert result is True

    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    @mock.patch('src.EmployeeService.Employee.check_availability')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_book_cab_not_available(self,inputs, mock_conn,mock_show_all_routes,mock_check_availability):
        inputs.side_effect = ['1', 's', 'd', '12:00']
        mock_show_all_routes.return_value = True
        mock_check_availability.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.book_cab()

        assert result is False

    def test_book_cab_unknown_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.book_cab()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.Main.create_connection')
    def test_cancel_booking_no_upcoming_bookings(self, mock_conn,mock_show_upcoming_bookings):

        mock_show_upcoming_bookings.return_value = []

        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeService.Employee.get_booking_by_id')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking_invalid_booking_id(self,inputs, mock_conn, mock_show_upcoming_bookings, mock_get_booking_by_id):
        inputs.side_effect = [1]
        mock_show_upcoming_bookings.return_value = ['something']
        mock_get_booking_by_id.return_value = []

        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False


    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    @mock.patch('src.EmployeeService.Employee.check_availability')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_book_cab_not_available(self,inputs, mock_conn,mock_show_all_routes,mock_check_availability):
        inputs.side_effect = ['1', 's', 'd', '12:00']
        mock_show_all_routes.return_value = True
        mock_check_availability.return_value = False
        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking_unknown_error(self,inputs, mock_conn, mock_show_upcoming_bookings):
        inputs.return_value = ['a']
        mock_show_upcoming_bookings.return_value = ['something']

        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False


    @mock.patch('src.EmployeeService.Employee.book_cab')
    @mock.patch('src.EmployeeService.Employee.show_past_bookings')
    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeService.Employee.cancel_booking')
    @mock.patch('src.EmployeeService.input')
    def test_employee_tasks(self, inputs, mock_book_cab, mock_show_past_bookings, mock_show_upcoming_bookings,
                          mock_cancel_booking):
        inputs.side_effect = ['1', '2', '3', '4', '6', '5']
        test_class = EmployeeService.Employee()

        test_class.employee_tasks()

        mock_book_cab.assert_called_once_with()
        mock_show_past_bookings.assert_called_once_with()
        mock_show_upcoming_bookings.assert_called_once_with()
        mock_cancel_booking.assert_called_once_with()
