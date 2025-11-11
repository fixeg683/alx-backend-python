#!/usr/bin/env python3
"""
Unit tests for the utils module functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Dict, Tuple, Any

# Assuming utils is in the same directory or importable
# import utils # Uncomment this if utils is a separate module
# Since the problem statement only gives the function names,
# we'll assume they are available or define placeholders if necessary
# For the purpose of providing the answer, we will not define the
# utility functions but focus only on the tests as requested.

# --- Task 0: Parameterize a unit test ---
class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the utils.access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str], expected: Any) -> None:
        """Test that access_nested_map returns the expected value."""
        # The body of the test method should not be longer than 2 lines.
        # Assuming access_nested_map is imported from utils
        # self.assertEqual(utils.access_nested_map(nested_map, path), expected)
        # Using a placeholder since utils is not defined:
        self.assertEqual(access_nested_map_placeholder(nested_map, path), expected)
    
    # --- Task 1: Parameterize a unit test (Exception) ---
    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple[str], expected_exception: Any) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths,
        and checks the exception message.
        """
        # Determine the key that should raise the error for the message check
        if nested_map == {}:
            key = "a"
        elif path == ("a", "b"):
            key = "b"
        
        with self.assertRaisesRegex(expected_exception, f"'{key}'"):
            # Assuming access_nested_map is imported from utils
            # utils.access_nested_map(nested_map, path)
            # Using a placeholder since utils is not defined:
            access_nested_map_placeholder(nested_map, path)


# --- Task 2: Mock HTTP calls ---
class TestGetJson(unittest.TestCase):
    """
    Tests for the utils.get_json function, mocking HTTP requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        """
        Test that get_json returns the expected payload and the mocked
        requests.get is called once with the correct URL.
        """
        # Configure the Mock object returned by requests.get
        # It needs a .json() method that returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        # result = utils.get_json(test_url)
        # Using a placeholder since utils is not defined:
        result = get_json_placeholder(test_url)

        # Test that the mocked get method was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Test that the output is equal to test_payload
        self.assertEqual(result, test_payload)


# --- Task 3: Parameterize and patch (Memoize) ---
class TestMemoize(unittest.TestCase):
    """
    Tests for the utils.memoize decorator.
    """
    
    def test_memoize(self) -> None:
        """
        Test that when calling a memoized property twice, the decorated
        method is only called once.
        """
        # Define the TestClass internally
        class TestClass:
            def a_method(self) -> int:
                """Method to be mocked and checked for call count."""
                return 42

            # Assuming memoize is imported from utils
            # @utils.memoize
            # Using a placeholder since utils is not defined:
            @memoize_placeholder
            def a_property(self) -> int:
                """The property that uses memoization."""
                return self.a_method()

        # Patch 'TestClass.a_method'
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            
            # Test that the correct result is returned
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            
            # Test that a_method was only called once
            mock_method.assert_called_once()


# Placeholder functions for tasks that rely on utility functions not provided
# These are necessary so the test code runs/makes sense in isolation
def access_nested_map_placeholder(nested_map: Dict, path: Tuple[str]) -> Any:
    """Mock implementation for access_nested_map."""
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current

def get_json_placeholder(url: str) -> Dict:
    """Mock implementation for get_json - not used since requests.get is patched."""
    pass

def memoize_placeholder(func):
    """Mock implementation for memoize decorator."""
    attr_name = '_{}'.format(func.__name__)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return property(wrapper)

if __name__ == '__main__':
    unittest.main()