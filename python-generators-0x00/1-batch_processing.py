#!/usr/bin/env python3
"""
Task 2: Batch Processing Users
This script demonstrates fetching user data in batches
and processing each batch to filter users over the age of 25.
"""

import sqlite3

def stream_users_in_batches(batch_size=10):
    """
    Fetch rows from the 'user_data' table in batches using a generator.
    """
    conn = sqlite3.connect("airbnb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, country FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # ✅ Use yield instead of return

    conn.close()


def batch_processing(batch_size=10):
    """
    Process each batch and filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user[2] > 25]  # ✅ age > 25
        yield filtered_users  # ✅ use yield for generator output


if __name__ == "__main__":
    # Example usage
    for filtered_batch in batch_processing(batch_size=5):
        for user in filtered_batch:
            print(f"User ID: {user[0]}, Name: {user[1]}, Age: {user[2]}, Country: {user[3]}")
