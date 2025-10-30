#!/usr/bin/env python3
"""
Task 2: Batch Processing
========================

This script demonstrates how to process data in batches rather than all at once.
It is especially useful when handling large datasets to optimize memory and performance.

Author: Neuron Stars
Course: ALX Back-End Development
Project: Airbnb Clone Backend
"""

import time
import json
from typing import List

# Simulated dataset (this could come from a database or API)
USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com"},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com"},
    {"id": 5, "name": "Ethan Hunt", "email": "ethan@example.com"},
    {"id": 6, "name": "Frank Castle", "email": "frank@example.com"},
    {"id": 7, "name": "Grace Hopper", "email": "grace@example.com"},
    {"id": 8, "name": "Hannah Baker", "email": "hannah@example.com"},
    {"id": 9, "name": "Ian Fleming", "email": "ian@example.com"},
    {"id": 10, "name": "Jane Doe", "email": "jane@example.com"}
]


def batch_process(data: List[dict], batch_size: int):
    """
    Generator function that yields data in batches.

    Args:
        data (list): List of items to process.
        batch_size (int): Number of items per batch.

    Yields:
        list: A batch of items.
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def process_batch(batch: List[dict]):
    """
    Simulates processing a batch of user data.

    Args:
        batch (list): Batch of user records to process.
    """
    print(f"\n🔹 Processing batch of {len(batch)} users...")
    for user in batch:
        print(f"   ✔ Processed: {user['name']} ({user['email']})")
    time.sleep(1)  # Simulate processing delay


def main():
    """
    Main function for batch processing.
    """
    print("🚀 Starting batch processing of user data...\n")

    batch_size = 3  # You can adjust this for larger or smaller batch sizes

    for batch in batch_process(USERS, batch_size):
        process_batch(batch)

    print("\n✅ All user data processed successfully in batches.")


if __name__ == "__main__":
    main()
