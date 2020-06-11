import mock
from src import EmployeeRepository
from src.Models import BookingsModel


class TestEmployeeRepository:

    @mock.patch('src.DbConnection.create_connection')
    def test_employee_login(self, mock_conn):
        email = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1)
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.employee_login(email)

        assert result == ('email@gmail.com', 'pass', 1)

    @mock.patch('src.DbConnection.create_connection')
    def test_set_password(self, mock_conn):
        password = 'xyz'
        id = 1
        sql = "Update Employees SET password = '{}' WHERE id = {}".format(password, id)
        test_class = EmployeeRepository.EmployeeRepository()

        test_class.set_password(password, id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_get_booking_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('id', 'booking')
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.get_booking_by_id(1)

        assert result == ('id', 'booking')

    @mock.patch('src.DbConnection.create_connection')
    def test_show_past_bookings(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('booking_details',)]
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.show_past_bookings(1)

        assert result == [('booking_details',)]

    @mock.patch('src.DbConnection.create_connection')
    def test_show_all_routes(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('route', '1')]
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.show_all_routes()

        assert result == [('route', '1')]

    @mock.patch('src.DbConnection.create_connection')
    def test_show_upcoming_bookings(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('booking_details',)]
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.show_upcoming_bookings(1)

        assert result == [('booking_details',)]

    @mock.patch('src.DbConnection.create_connection')
    def test_check_availability(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('booking_details',)]
        test_class = EmployeeRepository.EmployeeRepository()

        result = test_class.check_availability("route_id",'source','destination','timings')

        assert result == [('booking_details',)]

    @mock.patch('src.DbConnection.create_connection')
    def test_book_cab(self, mock_conn):
        booking = BookingsModel(emp_id=1,route_id='xyz',cab_number='abc',source='s',destination='d',timings='00:00')
        sql = """INSERT INTO Bookings (emp_id,route_id,cab_number,source,destination,timings)
                                 VALUES ({},'{}','{}','{}','{}','{}')
                              """.format(booking.emp_id, booking.route_id, booking.cab_number, booking.source, booking.destination, booking.timings)
        test_class = EmployeeRepository.EmployeeRepository()

        test_class.book_cab(booking)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_decrement_seats(self, mock_conn):
        cab_num = 'xyz'
        route_id = '1'
        source = 'test_s'
        destination = 'test_d'
        time = '00:00'
        sql = '''
                    Update cab_routes Set seats_available = seats_available - 1 
                    where cab_number = "{}" and route_id = "{}" and timings = "{}" and
                    stop_stage between 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}") 
                    and 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}")
              '''.format(cab_num, route_id, time, cab_num, source, route_id, time, cab_num, destination, route_id, time)
        test_class = EmployeeRepository.EmployeeRepository()

        test_class.decrement_seats(cab_num, route_id, source, destination, time)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_increment_seats(self, mock_conn):
        cab_num = 'xyz'
        route_id = '1'
        source = 'test_s'
        destination = 'test_d'
        time = '00:00'
        sql = '''
                    Update cab_routes Set seats_available = seats_available + 1 
                    where cab_number = "{}" and route_id = "{}" and timings = "{}" and
                    stop_stage between 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}") 
                    and 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}")
                '''.format(cab_num, route_id, time, cab_num, source, route_id, time, cab_num, destination, route_id,
                           time)
        test_class = EmployeeRepository.EmployeeRepository()

        test_class.increment_seats(cab_num, route_id, source, destination, time)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_cancel_booking(self, mock_conn):
        booking_id = 1
        sql = '''Update Bookings set cancelled = "yes" where id = {}'''.format(booking_id)
        test_class = EmployeeRepository.EmployeeRepository()

        test_class.cancel_booking(booking_id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()