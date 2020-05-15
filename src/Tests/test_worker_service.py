import mock
from src import WorkerService


class TestWorkerService:

    @mock.patch('src.WorkerService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.WorkerService.input')
    def test_login_password_match(self, inputs,mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'pass'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com','pass',1)
        test_class = WorkerService.Worker()

        result = test_class.worker_login()

        assert result is True

    @mock.patch('src.WorkerService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.WorkerService.input')
    def test_login_password_mismatch(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', 'pass', 1)
        test_class = WorkerService.Worker()

        result = test_class.worker_login()

        assert result is False

    @mock.patch('src.WorkerService.getpass')
    @mock.patch('src.Main.create_connection')
    @mock.patch('src.WorkerService.input')
    def test_login_first_time(self, inputs, mock_conn, getpass):
        inputs.return_value = 'email@gmail.com'
        getpass.return_value = 'password'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = ('email@gmail.com', None, 1)
        test_class = WorkerService.Worker()

        result = test_class.worker_login()

        assert result is True

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.WorkerService.input')
    def test_login_invalid_user(self, inputs, mock_conn):
        inputs.return_value = 'email@gmail.com'
        mock_conn.return_value.cursor.return_value.fetchone.return_value = None
        test_class = WorkerService.Worker()

        result = test_class.worker_login()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_active_complaints(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(3, 'gas leakout', 'gas leakout comment', 3, 'WIP', 'entity', '2020-05-14 13:10:40')]
        test_class = WorkerService.Worker()

        result = test_class.show_active_complaints()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_active_complaints_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = WorkerService.Worker()

        result = test_class.show_active_complaints()

        assert result is False

    def test_show_active_complaints_unknown_error(self):
        test_class = WorkerService.Worker()

        result = test_class.show_active_complaints()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_complaint_history(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [(3, 'gas leakout', 'gas leakout comment', 3, 'WIP', 'entity', '2020-05-14 13:10:40')]
        test_class = WorkerService.Worker()

        result = test_class.show_complaint_history()

        assert result is True

    @mock.patch('src.Main.create_connection')
    def test_show_complaint_history_empty(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        test_class = WorkerService.Worker()

        result = test_class.show_complaint_history()

        assert result is False

    def test_show_complaint_history_unknown_error(self):
        test_class = WorkerService.Worker()

        result = test_class.show_complaint_history()

        assert result is False

    @mock.patch('src.Main.create_connection')
    def test_show_worker_profile(self, mock_conn):
        mock_conn.return_value.cursor.return_value.fetchone.return_value = (1, 'test', 'test@gmail.com', 'test', 'none', '2020-05-14 13:07:30')
        test_class = WorkerService.Worker()

        result = test_class.show_worker_profile()

        assert result is True

    def test_show_worker_profile_unknown_error(self):
        test_class = WorkerService.Worker()

        result = test_class.show_worker_profile()

        assert result is False

    @mock.patch('src.Main.create_connection')
    @mock.patch('src.WorkerService.input')
    def test_create_complaint(self, input, mock_conn):
        input.side_effect = ['accident', 'comment']
        test_class = WorkerService.Worker()

        result = test_class.create_complaint()

        assert result is True

    def test_create_complaint_failure(self):
        test_class = WorkerService.Worker()

        result = test_class.create_complaint()

        assert result is False

    @mock.patch('src.WorkerService.Worker.show_worker_profile')
    @mock.patch('src.WorkerService.Worker.show_active_complaints')
    @mock.patch('src.WorkerService.Worker.show_complaint_history')
    @mock.patch('src.WorkerService.Worker.create_complaint')
    @mock.patch('src.WorkerService.input')
    def test_worker_tasks(self, input, mock_create_complaint,mock_show_complaint_history,mock_show_active_complaints,mock_show_worker_profile):
        input.side_effect = ['1','2','3','4','6','5']
        test_class = WorkerService.Worker()

        test_class.worker_tasks()

        mock_create_complaint.assert_called_once_with()
        mock_show_complaint_history.assert_called_once_with()
        mock_show_active_complaints.assert_called_once_with()
        mock_show_worker_profile.assert_called_once_with()