#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from utils import access_nested_map


def parameterized_expand(cases):
    """Manual implementation of parameterized.expand decorator."""
    def decorator(test_method):
        def wrapper(self):
            for case in cases:
                if len(case) == 3:
                    nested_map, path, expected = case
                    with self.subTest(nested_map=nested_map, path=path, expected=expected):
                        test_method(self, nested_map, path, expected)
                else:
                    raise ValueError("Each case must have 3 elements")
        return wrapper
    return decorator


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized_expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
