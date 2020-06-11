import mock
from src import AdminRepository
from src.Models import EmployeeModel, CabModel, RouteModel, CabRouteModel


class TestAdminRepository:

    @mock.patch('src.DbConnection.create_connection')
    def test_admin_login(self, mock_conn):
        email = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1)
        test_class = AdminRepository.AdminRepository()

        result = test_class.admin_login(email)

        assert result == ('email@gmail.com', 'pass', 1)

    @mock.patch('src.DbConnection.create_connection')
    def test_create_employee(self, mock_conn):
        employee = EmployeeModel(name="test", email="test@gmail.com")
        sql = "INSERT INTO Employees (name,email) VALUES ('{}','{}')".format(employee.name, employee.email)
        test_class = AdminRepository.AdminRepository()

        test_class.create_employee(employee)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_get_employee_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass')
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_employee_by_id(1)

        assert result == ('email@gmail.com', 'pass')

    @mock.patch('src.DbConnection.create_connection')
    def test_update_employee(self, mock_conn):
        name = "test"
        email = "test@gmail.com"
        employee_id = 1

        sql = ''' UPDATE Employees
                  SET name = '{}',
                  email = '{}'                    
                  WHERE id = {}
              '''.format(name, email, employee_id)

        test_class = AdminRepository.AdminRepository()

        test_class.update_employee(name, email, employee_id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_delete_employee(self, mock_conn):
        employee_id = 1
        sql = 'DELETE FROM Employees WHERE id={}'.format(employee_id)
        test_class = AdminRepository.AdminRepository()

        test_class.delete_employee(employee_id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_show_all_employees(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('email@gmail.com', 'pass', 1)]
        test_class = AdminRepository.AdminRepository()

        result = test_class.show_all_employees()

        assert result == [('email@gmail.com', 'pass', 1)]

    @mock.patch('src.DbConnection.create_connection')
    def test_create_cab(self, mock_conn):
        cab = CabModel(cab_number="xyz", capacity=1)
        sql = """INSERT INTO Cabs (cab_number,capacity)
                 VALUES ('{}',{})
              """.format(cab.cab_number, cab.capacity)
        test_class = AdminRepository.AdminRepository()

        test_class.create_cab(cab)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_create_route(self, mock_conn):
        route = RouteModel(route="test")
        sql = """
                INSERT INTO Routes (route)
                VALUES ('{}')
              """.format(route.route)
        test_class = AdminRepository.AdminRepository()

        test_class.create_route(route)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_get_cab_by_id(self, mock_conn):
        cab_num = "xyz"
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('cab', 1)
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_cab_by_id(cab_num)

        assert result == ('cab', 1)

    @mock.patch('src.DbConnection.create_connection')
    def test_get_route_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('route', 1)
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_route_by_id(1)

        assert result == ('route', 1)

    @mock.patch('src.DbConnection.create_connection')
    def test_update_cab(self, mock_conn):
        capacity = 2
        cab_num = "xyz"
        sql = ''' UPDATE Cabs
                  SET capacity = {}                   
                  WHERE cab_number = "{}" 
              '''.format(capacity, cab_num)

        test_class = AdminRepository.AdminRepository()
        test_class.update_cab(capacity, cab_num)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_delete_cab(self, mock_conn):
        cab_num = "xyz"
        sql = 'DELETE FROM Cabs WHERE cab_number="{}"'.format(cab_num)
        test_class = AdminRepository.AdminRepository()

        test_class.delete_cab(cab_num)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_delete_route(self, mock_conn):
        route_id = 1
        sql = 'DELETE FROM Routes WHERE route_id={}'.format(route_id)
        test_class = AdminRepository.AdminRepository()

        test_class.delete_route(route_id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_show_all_cabs(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('cab', '1')]
        test_class = AdminRepository.AdminRepository()

        result = test_class.show_all_cabs()

        assert result == [('cab', '1')]

    @mock.patch('src.DbConnection.create_connection')
    def test_show_all_routes(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('route', '1')]
        test_class = AdminRepository.AdminRepository()

        result = test_class.show_all_routes()

        assert result == [('route', '1')]

    @mock.patch('src.DbConnection.create_connection')
    def test_create_cab_route(self, mock_conn):
        cab_route = CabRouteModel(cab_number="x", route_id='y', stop_name='z', stop_stage=1, timings="00:00")
        sql = """Insert into cab_routes(cab_number,route_id,stop_name,stop_stage,timings)
                 Values('{}','{}','{}',{},'{}')
              """.format(cab_route.cab_number, cab_route.route_id, cab_route.stop_name, cab_route.stop_stage,
                         cab_route.timings)
        test_class = AdminRepository.AdminRepository()

        test_class.create_cab_route(cab_route)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_get_cab_route_by_cab_num(self, mock_conn):
        cab_num = 'abc'
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('cab_route', '1')]
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_cab_route_by_cab_num(cab_num)

        assert result == [('cab_route', '1')]

    @mock.patch('src.DbConnection.create_connection')
    def test_get_all_cab_routes(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('cab_route', '1')]
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_all_cab_routes()

        assert result == [('cab_route', '1')]

    @mock.patch('src.DbConnection.create_connection')
    def test_get_cab_route_by_id(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('cab_route', 1)
        test_class = AdminRepository.AdminRepository()

        result = test_class.get_cab_route_by_id(1)

        assert result == ('cab_route', 1)

    @mock.patch('src.DbConnection.create_connection')
    def test_update_cab_route(self, mock_conn):
        updated_cab_num = "xyz"
        route_id = "1"
        stop_name = "test"
        stop_stage = 1
        timings = "00:00"
        id = 1
        sql = ''' UPDATE cab_routes
                  SET cab_number = '{}' ,
                  route_id = '{}' ,
                  stop_name = '{}',
                  stop_stage = {},
                  timings = '{}'
                  WHERE id = {}'''.format(updated_cab_num, route_id, stop_name, stop_stage, timings, id)
        test_class = AdminRepository.AdminRepository()

        test_class.update_cab_route(updated_cab_num, route_id, stop_name, stop_stage, timings, id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)
        mock_conn.return_value.commit.assert_called_once_with()

    @mock.patch('src.DbConnection.create_connection')
    def test_delete_cab_route(self, mock_conn):
        cab_num = "xyz"
        route_id = 'abc'
        sql = 'DELETE FROM cab_routes WHERE cab_number="{}" and route_id = "{}"'.format(cab_num, route_id)
        test_class = AdminRepository.AdminRepository()

        test_class.delete_cab_route(cab_num, route_id)

        mock_conn.return_value.cursor.return_value.execute.assert_called_once_with(sql)

    @mock.patch('src.DbConnection.create_connection')
    def test_show_emp_bookings(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [('id', 'booking_details')]

        test_class = AdminRepository.AdminRepository()

        result = test_class.show_emp_bookings(1)

        assert result == [('id', 'booking_details')]

    @mock.patch('src.DbConnection.create_connection')
    def test_show_total_bookings_day(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('day', 100)

        test_class = AdminRepository.AdminRepository()
        result = test_class.show_total_bookings_day('2020-01-01')

        assert result == ('day', 100)

    @mock.patch('src.DbConnection.create_connection')
    def test_show_total_bookings_week(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('week', 100)

        test_class = AdminRepository.AdminRepository()

        result = test_class.show_total_bookings_week(1)

        assert result == ('week', 100)

    @mock.patch('src.DbConnection.create_connection')
    def test_show_total_bookings_month(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('month', 100)

        test_class = AdminRepository.AdminRepository()

        result = test_class.show_total_bookings_month(1)

        assert result == ('month', 100)
