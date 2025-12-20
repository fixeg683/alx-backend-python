#!/usr/bin/python3
"""
Task 3: Lazy Loading Paginated Data
===================================

Objective:
-----------
Simulate fetching paginated data from the users database using a generator
to lazily load each page — only loading data when required.

Functions:
-----------
- paginate_users(page_size, offset): fetches a page of users from MySQL.
- lazy_pagination(page_size): lazily loads users page by page using yield.

Requirements:
--------------
- Must use only one loop.
- Must use the yield generator.
- Must import seed.py for database connection.

Author: Neuron Stars
Course: ALX Backend - Python
Project: python-generators-0x00
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the MySQL database.

    Args:
        page_size (int): Number of users to fetch per page.
        offset (int): Offset for pagination.

    Returns:
        list[dict]: List of user records.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function that lazily loads pages of users.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list[dict]: One page of user data per iteration.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    # Demo: print first few users from lazy pagination
    try:
        for page in lazy_pagination(100):
            for user in page:
                print(user)
    except KeyboardInterrupt:
        print("\nStopped by user.")
