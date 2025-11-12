#!/usr/bin/env python3
"""
Unit tests for the utils module.
Tests the memoize decorator.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Class for testing the memoize decorator in utils.py."""

    def test_memoize(self):
        """Test that memoize properly caches the method output."""

        class TestClass:
            """Simple class to test memoization behavior."""

            def a_method(self):
                """Return a constant value."""
                return 42

            @memoize
            def a_property(self):
                """Method decorated with memoize."""
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()

            # First and second calls
            result1 = obj.a_property
            result2 = obj.a_property

            # Assertions
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
