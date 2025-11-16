#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from utils import access_nested_map


# Simple parameterized implementation
def expand(cases):
    def decorator(f):
        def wrapper(self):
            for args in cases:
                f(self, *args)
        return wrapper
    return decorator


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
