import sqlite3
import mock
from freezegun import freeze_time
from src import EmployeeService


class TestEmployeeService:

    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.employee_login')
    @mock.patch('src.EmployeeService.input')
    def test_login_password_match(self, inputs, mock_repository, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_repository.return_value = ('email@gmail.com', 'pass', 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is True

    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.employee_login')
    @mock.patch('src.EmployeeService.input')
    def test_login_password_mismatch(self, inputs, mock_repository, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_repository.return_value = ('email@gmail.com', 'pass', 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.set_password')
    @mock.patch('src.EmployeeService.getpass')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.employee_login')
    @mock.patch('src.EmployeeService.input')
    def test_login_first_time(self, inputs, mock_repository, getpass, mock_set_password):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_repository.return_value = ('email@gmail.com', None, 1, 'TeamName')
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is True

    @mock.patch('src.EmployeeRepository.EmployeeRepository.employee_login')
    @mock.patch('src.EmployeeService.input')
    def test_login_invalid_user(self, inputs, mock_repository):
        inputs.return_value = 'email@gmail.com'
        mock_repository.return_value = None
        test_class = EmployeeService.Employee()

        result = test_class.employee_login()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_past_bookings')
    def test_show_past_bookings(self, mock_repository):
        mock_repository.return_value = [
            ('2020-05-28', '21:00', 'test', 'source', 'destination', 1)]
        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is True

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_past_bookings')
    def test_show_past_bookings_empty(self, mock_repository):
        mock_repository.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_past_bookings')
    def test_show_past_bookings_error(self, mock_repository):
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        test_class = EmployeeService.Employee()

        result = test_class.show_past_bookings()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_upcoming_bookings')
    def test_show_upcoming_bookings(self, mock_repository):
        mock_repository.return_value = [
            ('2020-05-28', '21:00', 'test', 'source', 'destination', 1)]
        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is True

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_upcoming_bookings')
    def test_show_upcoming_bookings_empty(self, mock_repository):
        mock_repository.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_upcoming_bookings')
    def test_show_upcoming_bookings_error(self, mock_repository):
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        test_class = EmployeeService.Employee()

        result = test_class.show_upcoming_bookings()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_all_routes')
    def test_show_all_routes(self, mock_repository):
        mock_repository.return_value = [(1, 'test')]
        test_class = EmployeeService.Employee()

        result = test_class.show_all_routes()

        assert result is True

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_all_routes')
    def test_show_all_routes_empty(self, mock_repository):
        mock_repository.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.show_all_routes()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.show_all_routes')
    def test_show_all_routes_error(self, mock_repository):
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        test_class = EmployeeService.Employee()

        result = test_class.show_all_routes()

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.check_availability')
    def test_check_availability(self, mock_repository):
        mock_repository.return_value = [('cab123', '12:00:00', 2, 'stop', 2)]
        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is True

    @mock.patch('src.EmployeeRepository.EmployeeRepository.check_availability')
    def test_check_availability_empty(self, mock_repository):
        mock_repository.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is False

    def test_check_availability_error(self):
        test_class = EmployeeService.Employee()

        result = test_class.check_availability(1, 'k', 'd', '10:00')

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.get_booking_by_id')
    def test_get_booking_by_id(self, mock_repository):
        mock_repository.return_value = [
            ('2020-01-01', '12:00:00', 'cab123', 1, 'source', 'destination')]
        test_class = EmployeeService.Employee()

        result = test_class.get_booking_by_id(1)

        assert result == [('2020-01-01', '12:00:00', 'cab123', 1, 'source', 'destination')]

    @mock.patch('src.EmployeeRepository.EmployeeRepository.get_booking_by_id')
    def test_get_booking_by_id_invalid_id(self, mock_repository):
        mock_repository.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.get_booking_by_id(1)

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.get_booking_by_id')
    def test_get_booking_by_id_error(self,mock_repository):
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        test_class = EmployeeService.Employee()

        result = test_class.get_booking_by_id('a')

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.decrement_seats')
    def test_decrement_seats(self, mock_repository):
        cab_num = 'cab123'
        route_id = '1'
        source = 's'
        destination = 'd'
        time = '12:00'
        test_class = EmployeeService.Employee()

        test_class.decrement_seats(cab_num, route_id, source, destination, time)

        mock_repository.assert_called_once_with(cab_num, route_id, source, destination, time)

    @mock.patch('src.EmployeeRepository.EmployeeRepository.decrement_seats')
    def test_decrement_seats_error(self, mock_repository):
        test_class = EmployeeService.Employee()
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')

        result = test_class.decrement_seats('cab123', 1, 's', 'd', '12:00')

        assert result is False

    @mock.patch('src.EmployeeRepository.EmployeeRepository.increment_seats')
    def test_increment_seats(self, mock_repository):
        cab_num = 'cab123'
        route_id = '1'
        source = 's'
        destination = 'd'
        time = '12:00'
        test_class = EmployeeService.Employee()

        test_class.increment_seats(cab_num, route_id, source, destination, time)

        mock_repository.assert_called_once_with(cab_num, route_id, source, destination, time)

    @mock.patch('src.EmployeeService.EmployeeRepository.increment_seats')
    def test_increment_seats_error(self, mock_repository):
        test_class = EmployeeService.Employee()
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        result = test_class.increment_seats('cab123', 1, 's', 'd', '12:00')

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    @mock.patch('src.EmployeeService.Employee.check_availability')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.book_cab')
    @mock.patch('src.EmployeeService.input')
    def test_book_cab(self, inputs, mock_repository, mock_show_all_routes, mock_check_availability):
        inputs.side_effect = ['1', 's', 'd', '12:00', 'cab', '13:00']
        mock_show_all_routes.return_value = True
        mock_check_availability.return_value = True
        test_class = EmployeeService.Employee()

        result = test_class.book_cab()

        assert result is True

    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    @mock.patch('src.EmployeeService.Employee.check_availability')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.book_cab')
    @mock.patch('src.EmployeeService.input')
    def test_book_cab_not_available(self, inputs, mock_repository, mock_check_availability, mock_show_all_routes):
        inputs.side_effect = ['1', 's', 'd', '12:00']
        mock_check_availability.return_value = []
        test_class = EmployeeService.Employee()
        result = test_class.book_cab()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_all_routes')
    def test_book_cab_error(self, mock_repository):
        mock_repository.side_effect = sqlite3.OperationalError(mock.Mock(), 'db lock')
        test_class = EmployeeService.Employee()

        result = test_class.book_cab()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.cancel_booking')
    def test_cancel_booking_no_upcoming_bookings(self, mock_repository, mock_show_upcoming_bookings):
        mock_show_upcoming_bookings.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeService.Employee.get_booking_by_id')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.cancel_booking')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking_invalid_booking_id(self, inputs, mock_repository,
                                               mock_get_booking_by_id, mock_show_upcoming_bookings):
        inputs.side_effect = [1]
        mock_show_upcoming_bookings.return_value = True
        mock_get_booking_by_id.return_value = []
        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False

    @freeze_time("2020-01-01 01:00:00")
    @mock.patch('src.EmployeeService.Employee.increment_seats')
    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeService.Employee.get_booking_by_id')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.cancel_booking')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking(self, inputs, mock_repository, mock_get_booking_by_id, mock_show_upcoming_bookings,
                            mock_increment_seats):
        inputs.side_effect = [1]
        mock_show_upcoming_bookings.return_value = True
        mock_get_booking_by_id.return_value = ('2020-01-01', '10:00', 'cab123', 1, 'source', 'destination')
        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is True

    @freeze_time("2020-01-01 09:35:00")
    @mock.patch('src.EmployeeService.Employee.increment_seats')
    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeService.Employee.get_booking_by_id')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.cancel_booking')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking_time_constraint_failure(self, inputs, mock_repository, mock_get_booking_by_id,
                                                    mock_show_upcoming_bookings,
                                                    mock_increment_seats):
        inputs.side_effect = [1]
        mock_show_upcoming_bookings.return_value = True
        mock_get_booking_by_id.return_value = ('2020-01-01', '10:00', 'cab123', 1, 'source', 'destination')
        test_class = EmployeeService.Employee()

        result = test_class.cancel_booking()

        assert result is False

    @mock.patch('src.EmployeeService.Employee.show_upcoming_bookings')
    @mock.patch('src.EmployeeRepository.EmployeeRepository.cancel_booking')
    @mock.patch('src.EmployeeService.input')
    def test_cancel_booking_error(self, inputs, mock_repository, mock_show_upcoming_bookings):
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
