#!/usr/bin/python3
"""
Task 1: Generator that streams rows from an SQL database one by one
===================================================================

Objective:
-----------
Use a Python generator (`yield`) to stream rows from the `user_data`
table one by one.

Requirements:
-------------
- Use the yield statement.
- Use only one loop.
- Return rows as dictionaries with user details.
"""

import seed


def stream_users():
    """
    Generator function that streams rows one by one from the user_data table.
    Yields:
        dict: Each row containing user_id, name, email, and age.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()


# Optional test for standalone execution
if __name__ == "__main__":
    from itertools import islice
    for user in islice(stream_users(), 5):
        print(user)
