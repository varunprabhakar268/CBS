import mock
from src import WorkerService


class TestWorkerService:

    # @mock.patch('Main.create_connection')
    # def test_update_project_member_attendance(self, mock_conn):
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.commit.return_value = True
    #     project_member_id = 1
    #
    #     result = WorkerService.update_project_member_attendance(mock_conn, project_member_id)
    #
    #     assert result == True
    #
    # @mock.patch('Main.create_connection')
    # def test_update_project_member_wage(self, mock_conn):
    #     project_member_id = 1
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.commit.return_value = True
    #
    #     result = WorkerService.update_project_member_wage(mock_conn, project_member_id)
    #
    #     assert result == True
    #
    # @mock.patch('Main.create_connection')
    # def test_show_member_details(self, mock_conn):
    #     dummy_object = ['MemberName', 'email@gmail.com', 22, 'male', 'place', 'address', 1000]
    #     member_id = 1
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.cursor().fetchone.return_value = dummy_object
    #
    #     result = WorkerService.show_member_details(mock_conn, member_id)
    #
    #     assert result == dummy_object
    #
    # @mock.patch('Main.create_connection')
    # def test_file_complaint(self, mock_conn):
    #     mock_conn.cursor().execute.return_value = True
    #     bdo_id = 1
    #     gpm_id = 1
    #     member_id = 1
    #     issue = 'test issue'
    #     result = WorkerService.file_complaint(mock_conn, bdo_id, gpm_id, member_id, issue)
    #
    #     assert result == True

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



