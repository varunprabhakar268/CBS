import sqlite3
from sqlite3 import Error
from src import Schema


def create_connection():
    """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
    db_file = "cbs_db.sqlite"
    try:
        conn = sqlite3.connect(db_file)
        Schema.create_tables(conn)
        return conn
    except Error as e:
        print(e)
        return False
