import sqlite3

class WorkWithDb:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def get_cursor(self):
        if self.conn is None:
            self.connect()
        return self.conn.cursor()

    def commit_and_close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute_query(self, query, params=None):
        cursor = self.get_cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
