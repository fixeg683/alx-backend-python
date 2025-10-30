#!/usr/bin/python3
"""
Task 4: Memory-Efficient Aggregation with Generators
====================================================

Objective:
-----------
Use a generator to compute a memory-efficient aggregate function (average age)
for a large dataset without loading it entirely into memory.

Functions:
-----------
- stream_user_ages(): Yields user ages one by one from the MySQL database.
- calculate_average_age(): Consumes the generator to calculate average age.

Requirements:
--------------
- Must use no more than two loops.
- Must NOT use the SQL AVERAGE() function.
- Must use yield for generator-based streaming.

Author: Neuron Stars
Course: ALX Backend - Python
Project: python-generators-0x00
"""

import seed


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.

    Yields:
        int: The age of each user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates and prints the average age of users using the generator.

    This function consumes the `stream_user_ages` generator efficiently
    without loading all records into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        avg_age = total_age / count
        print(f"Average age of users: {avg_age:.2f}")
    else:
        print("No user data found.")


if __name__ == "__main__":
    calculate_average_age()
