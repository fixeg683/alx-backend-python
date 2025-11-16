#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    def test_access_nested_map(self):
        """Test access_nested_map with valid paths."""
        test_cases = [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
        
        for nested_map, path, expected in test_cases:
            with self.subTest(nested_map=nested_map, path=path):
                self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
