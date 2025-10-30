#!/usr/bin/env python3
"""
Task 1: Stream Users
====================

This script streams all user data efficiently (e.g., from a database or API)
and prints it in real time without loading everything into memory at once.

It demonstrates generator-based streaming in Python for handling large datasets.

Author: Neuron Stars
Course: ALX Back-End Development
Project: Airbnb Clone Backend
"""

import time
import json

# Simulated user data source (could be replaced by a real DB query or API call)
USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "host"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "guest"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "role": "host"},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com", "role": "guest"},
    {"id": 5, "name": "Ethan Hunt", "email": "ethan@example.com", "role": "host"},
]


def stream_users(users):
    """
    Generator function that yields one user record at a time.

    Args:
        users (list): List of user dictionaries.

    Yields:
        dict: A user record.
    """
    for user in users:
        yield user
        time.sleep(0.5)  # Simulate streaming delay


def main():
    """
    Main entry point for the script.
    Streams all users and prints them in real-time JSON format.
    """
    print("🔄 Streaming user data...\n")
    for user in stream_users(USERS):
        print(json.dumps(user, indent=4))
    print("\n✅ All users have been streamed successfully.")


if __name__ == "__main__":
    main()
