import mock
from src import DbConnection


class TestDbConnection:

    @mock.patch('src.Schema.create_tables')
    @mock.patch('src.DbConnection.sqlite3.connect')
    def test_create_connection(self, mock_conn, mock_schema):
        mock_conn.return_value = 'success'

        result = DbConnection.create_connection()

        assert result == 'success'
