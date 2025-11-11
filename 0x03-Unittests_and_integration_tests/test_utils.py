#!/usr/bin/env python3
"""
Unit tests for utils.py module.
Covers access_nested_map, get_json, and memoize.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator in utils module."""

    def test_memoize(self):
        """Test that memoize caches method output correctly."""

        class TestClass:
            """Simple class to test memoization behavior."""

            def a_method(self):
                """A simple method returning a constant."""
                return 42

            @memoize
            def a_property(self):
                """Method decorated with memoize."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
