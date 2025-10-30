#!/usr/bin/env python3
"""
Task 4: Stream User Ages
Compute the average user age without using SQL's AVG() function.
"""

import sqlite3

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    conn = sqlite3.connect("airbnb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")  # ✅ No AVG() used

    while True:
        rows = cursor.fetchmany(10)
        if not rows:
            break
        for (age,) in rows:
            yield age  # ✅ Yield ages one by one

    conn.close()


def compute_average_age():
    """
    Computes the average age manually using streamed data.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0

    average_age = total_age / count  # ✅ Manual average calculation
    return average_age


if __name__ == "__main__":
    avg_age = compute_average_age()
    print(f"The average user age is: {avg_age:.2f}")
