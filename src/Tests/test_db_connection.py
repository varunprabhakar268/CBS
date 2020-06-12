import sqlite3

import mock
from src import DbConnection


class TestDbConnection:

    @mock.patch('src.Schema.create_tables')
    @mock.patch('src.DbConnection.sqlite3.connect')
    def test_create_connection(self, mock_conn, mock_schema):
        mock_conn.return_value = 'success'

        result = DbConnection.create_connection()

        assert result == 'success'

    @mock.patch('src.DbConnection.sqlite3.connect')
    def test_create_connection_fail(self, mock_conn):
        mock_conn.side_effect = sqlite3.Error

        result = DbConnection.create_connection()

        assert result is False
