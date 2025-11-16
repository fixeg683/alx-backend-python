# Unit Tests and Integration Tests

This project focuses on understanding and implementing unit tests and integration tests in Python using the `unittest` framework. It covers key testing concepts including mocking, parametrization, and fixtures.

## Learning Objectives

By the end of this project, you will be able to explain to anyone:

- The difference between unit and integration tests
- Common testing patterns such as mocking, parametrization, and fixtures
- How to write comprehensive test suites for Python applications

## Project Structure

```
0x03-Unittests_and_integration_tests/
├── utils.py
├── client.py
├── fixtures.py
├── test_utils.py
└── test_client.py
```

## Key Concepts

### Unit Tests vs Integration Tests

**Unit Tests:**
- Test individual components in isolation
- Mock external dependencies
- Fast execution
- Focus on specific functionality

**Integration Tests:**
- Test how components work together
- Minimal mocking of external dependencies
- Test entire workflows
- Ensure components integrate correctly

### Common Testing Patterns

#### 1. Mocking
- Replace real dependencies with controlled test doubles
- Prevent external API calls during testing
- Control test scenarios and responses

```python
@patch('module.function')
def test_method(self, mock_function):
    mock_function.return_value = expected_result
    # Test implementation
```

#### 2. Parametrization
- Run the same test with different inputs
- Reduce code duplication
- Comprehensive test coverage

```python
@parameterized.expand([
    (input1, expected1),
    (input2, expected2),
])
def test_method(self, input, expected):
    result = function_under_test(input)
    self.assertEqual(result, expected)
```

#### 3. Fixtures
- Provide test data and setup/teardown functionality
- Reusable across multiple tests
- Consistent test environment

```python
@parameterized_class([
    {'fixture_data': test_data},
])
class TestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup before all tests
        pass
    
    @classmethod
    def tearDownClass(cls):
        # Cleanup after all tests
        pass
```

## Files Description

### `utils.py`
Contains utility functions:
- `access_nested_map`: Access nested dictionaries with key paths
- `get_json`: Fetch JSON from remote URLs
- `memoize`: Decorator to cache method results

### `client.py`
Implements `GithubOrgClient` class for interacting with GitHub organization API:
- Fetch organization details
- Get public repositories
- Filter repositories by license

### `fixtures.py`
Contains test payload data for integration tests, including:
- Organization payload
- Repository payload
- Expected repository lists

### `test_utils.py`
Unit tests for utility functions:
- Test `access_nested_map` with valid and invalid paths
- Test `get_json` with mocked HTTP requests
- Test `memoize` decorator caching behavior

### `test_client.py`
Tests for `GithubOrgClient`:
- Unit tests for individual methods
- Integration tests with mocked API responses
- License filtering functionality

## Testing Requirements

- All files must be executable
- Code must follow pycodestyle (version 2.5)
- All modules, classes, and functions must have proper documentation
- Functions and coroutines must be type-annotated
- Tests should be comprehensive and cover edge cases

## Usage

Run all tests:
```bash
python -m unittest discover
```

Run specific test file:
```bash
python -m unittest test_utils.py
```

Run with verbose output:
```bash
python -m unittest discover -v
```

## Key Assertion Methods

- `assertEqual(a, b)`: Check if a equals b
- `assertRaises(Exception)`: Verify exception is raised
- `assertTrue(x)`: Check if x is True
- `assertFalse(x)`: Check if x is False
- `assertIsNone(x)`: Check if x is None
- `assertIn(a, b)`: Check if a is in b

## Mocking Techniques

- `patch`: Replace objects during testing
- `return_value`: Set mock return value
- `side_effect`: Define complex mock behavior
- `assert_called_once`: Verify mock was called exactly once
- `PropertyMock`: Mock properties specifically

This project demonstrates professional testing practices essential for building reliable and maintainable Python applications.
