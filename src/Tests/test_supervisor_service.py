import mock
from src import SupervisorService


class TestSupervisorService:

    @mock.patch('src.SupervisorService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.SupervisorService.input')
    def test_login_password_match(self, inputs,mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com','pass',1,'TeamName')
        test_class = SupervisorService.Supervisor()

        result = test_class.supervisor_login()

        assert result is True

    @mock.patch('src.SupervisorService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.SupervisorService.input')
    def test_login_password_mismatch(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com','pass',1,'TeamName')
        test_class = SupervisorService.Supervisor()

        result = test_class.supervisor_login()

        assert result is False

    @mock.patch('src.SupervisorService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.SupervisorService.input')
    def test_login_first_time(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com',None,1,'TeamName')
        test_class = SupervisorService.Supervisor()

        result = test_class.supervisor_login()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.SupervisorService.input')
    def test_login_invalid_user(self, inputs, mock_conn):
        inputs.return_value = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = None
        test_class = SupervisorService.Supervisor()

        result = test_class.supervisor_login()

        assert result is False