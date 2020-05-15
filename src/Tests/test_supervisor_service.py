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

    @mock.patch('src.Main.create_connection')
    def test_show_complaint(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(1, 'gas leakout', 'test comments')]
        test_class = SupervisorService.Supervisor()

        result = test_class.show_complaint()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_complaint_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = SupervisorService.Supervisor()

        result = test_class.show_complaint()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_reports(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(1, 1, 'soul', 'short circuit', 'test details', 10, 5, 'approved', '2020-05-14 12:41:24')]
        test_class = SupervisorService.Supervisor()

        result = test_class.show_reports()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_reports_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = SupervisorService.Supervisor()

        result = test_class.show_reports()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.SupervisorService.Supervisor.show_complaint')
    @mock.patch('src.SupervisorService.input')
    def test_create_report(self, input, mock_show_complaint,mock_conn):
        input.side_effect = [1,'cause', 'details',10,10]
        test_class = SupervisorService.Supervisor()

        result = test_class.create_report()

        assert result is True

    def test_create_report_failure(self):
        test_class = SupervisorService.Supervisor()

        result = test_class.create_report()

        assert result is False

    @mock.patch('src.SupervisorService.Supervisor.show_reports')
    @mock.patch('src.SupervisorService.Supervisor.create_report')
    @mock.patch('src.SupervisorService.Supervisor.show_complaint')
    @mock.patch('src.SupervisorService.input')
    def test_worker_tasks(self, inputs, mock_show_complaint,mock_create_report,mock_show_reports):
        inputs.side_effect = ['1','2','3','6','4']
        test_class = SupervisorService.Supervisor()

        test_class.supervisor_tasks()

        mock_show_complaint.assert_called_once_with()
        mock_create_report.assert_called_once_with()
        mock_show_reports.assert_called_once_with()
