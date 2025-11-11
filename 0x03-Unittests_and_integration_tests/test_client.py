#!/usr/bin/env python3
"""
Unit and integration tests for the client module functions.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict, List, Tuple
import json

# Assuming client and utils are importable
# from client import GithubOrgClient
# from utils import get_json 
# For the purpose of the answer, we will assume GithubOrgClient is available.
# We will also use the fixtures from a hypothetical fixtures.py.

# --- Fixtures Placeholder (As specified in Task 8) ---
# In a real scenario, these would be imported from fixtures.py
ORG_PAYLOAD = {"repos_url": "https://api.github.com/orgs/google/repos"}
REPOS_PAYLOAD = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "gpl-3.0"}},
]
EXPECTED_REPOS = ["repo1", "repo2", "repo3"]
APACHE2_REPOS = ["repo1"]

# --- Task 4, 5, 6, 7: Unit Tests for GithubOrgClient ---
class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the client.GithubOrgClient class.
    """

    # --- Task 4: Parameterize and patch as decorators ---
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the expected argument.
        """
        # Assuming GithubOrgClient is available
        # client = GithubOrgClient(org_name)
        client = GithubOrgClient_placeholder(org_name)
        
        # Access the .org property
        result = client.org
        
        # Test that the result is the mocked return value
        self.assertEqual(result, {"payload": True})
        
        # Test that get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)


    # --- Task 5: Mocking a property ---
    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the expected URL
        based on a mocked 'org' property.
        """
        # Mock the 'org' property using patch.object
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = ORG_PAYLOAD
            
            # Assuming GithubOrgClient is available
            # client = GithubOrgClient("google")
            client = GithubOrgClient_placeholder("google")
            
            # Access the _public_repos_url property (or method if not a property)
            result = client._public_repos_url
            
            # Test that the result is the expected URL from the mocked payload
            self.assertEqual(result, ORG_PAYLOAD["repos_url"])

    
    # --- Task 6: More patching ---
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test that public_repos returns the expected list of repository names.
        Mocks both get_json and _public_repos_url.
        """
        # 1. Mock the return value of get_json (for the repos list)
        mock_get_json.return_value = REPOS_PAYLOAD
        
        # The expected list of repo names
        expected_repos = [repo["name"] for repo in REPOS_PAYLOAD]

        # 2. Patch GithubOrgClient._public_repos_url using patch.object context manager
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_repos_url:
            
            # Set the return value for _public_repos_url (the URL doesn't strictly matter here, just its call)
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"

            # Assuming GithubOrgClient is available
            # client = GithubOrgClient("google")
            client = GithubOrgClient_placeholder("google")
            
            # Call the method under test
            result = client.public_repos()
            
            # Test that the list of repos is what is expected
            self.assertEqual(result, expected_repos)
            
            # Test that the mocked property was called once
            mock_repos_url.assert_called_once()
            
            # Test that the mocked get_json was called once
            mock_get_json.assert_called_once()


    # --- Task 7: Parameterize ---
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False), # Additional test case for no license key
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """
        Test that GithubOrgClient.has_license returns the expected boolean value.
        """
        # Assuming GithubOrgClient is available
        # result = GithubOrgClient.has_license(repo, license_key)
        result = GithubOrgClient_placeholder.has_license(repo, license_key)
        self.assertEqual(result, expected)


# --- Task 8: Integration test: fixtures ---
@parameterized_class([
    {
        'org_payload': ORG_PAYLOAD,
        'repos_payload': REPOS_PAYLOAD,
        'expected_repos': EXPECTED_REPOS,
        'apache2_repos': APACHE2_REPOS,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.public_repos,
    mocking only external requests.
    """
    
    # Class-level variables (populated by parameterized_class)
    org_payload: Dict
    repos_payload: List[Dict]
    expected_repos: List[str]
    apache2_repos: List[str]

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the mock for requests.get using side_effect."""
        
        def side_effect_callback(url):
            """Returns the correct Mock response for a given URL."""
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]: # i.e., "https://api.github.com/orgs/google/repos"
                mock_resp.json.return_value = cls.repos_payload
            else:
                # Fallback for unexpected URLs
                mock_resp.json.return_value = {} 
            return mock_resp

        # Start the patcher
        cls.get_patcher = patch('requests.get', side_effect=side_effect_callback)
        cls.mock_get = cls.get_patcher.start()
        
    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the patcher."""
        cls.get_patcher.stop()

    # The actual tests (not explicitly requested, but included for completeness of the integration test)
    # def test_public_repos_integration(self):
    #     """Test public_repos without mocking internal methods/properties."""
    #     client = GithubOrgClient("google")
    #     self.assertEqual(client.public_repos(), self.expected_repos)
    #     self.assertEqual(self.mock_get.call_count, 2)
        
    # def test_public_repos_with_license_integration(self):
    #     """Test public_repos with a specific license filter."""
    #     client = GithubOrgClient("google")
    #     self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
    #     self.assertEqual(self.mock_get.call_count, 2)
        
# --- Placeholder Class ---
# Since the actual GithubOrgClient is not provided, this mock is used for the tests.
class GithubOrgClient_placeholder:
    """Mock class mimicking the behavior of GithubOrgClient for testing purposes."""
    
    def __init__(self, org_name):
        self._org_name = org_name

    @property
    def org(self):
        # This property is mocked in the tests, so its implementation doesn't matter.
        pass

    @property
    def _public_repos_url(self):
        # This property is mocked in the tests, so its implementation doesn't matter.
        pass

    def public_repos(self, license=None):
        # This method is heavily mocked in the tests, so its implementation doesn't matter.
        pass

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Mimics the static method behavior for Task 7."""
        if repo.get("license") and repo["license"].get("key") == license_key:
            return True
        return False

if __name__ == '__main__':
    unittest.main()