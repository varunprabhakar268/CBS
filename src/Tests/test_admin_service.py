from datetime import datetime, timedelta

import mock
from src import AdminService


class TestAdminService:
    @mock.patch('src.AdminService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.AdminService.input')
    def test_login_password_match(self, inputs,mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com','pass',1)
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