#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Custom context manager that executes a provided query automatically."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Connect to DB, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close DB connection after use."""
        if self.conn:
            self.conn.close()


# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    print(results)
