#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    def test_access_nested_map_single(self):
        """Test single level access."""
        nested_map = {"a": 1}
        path = ("a",)
        self.assertEqual(access_nested_map(nested_map, path), 1)

    def test_access_nested_map_nested_1(self):
        """Test first level of nested access."""
        nested_map = {"a": {"b": 2}}
        path = ("a",)
        self.assertEqual(access_nested_map(nested_map, path), {"b": 2})

    def test_access_nested_map_nested_2(self):
        """Test second level of nested access."""
        nested_map = {"a": {"b": 2}}
        path = ("a", "b")
        self.assertEqual(access_nested_map(nested_map, path), 2)


if __name__ == '__main__':
    unittest.main()
