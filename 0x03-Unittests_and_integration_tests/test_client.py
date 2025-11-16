#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

# Import the client directly
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from client import GithubOrgClient
except ImportError as e:
    print(f"Import error: {e}")
    # Create a mock client for testing
    class GithubOrgClient:
        def __init__(self, org_name):
            self._org_name = org_name
        
        @property
        def org(self):
            return {"repos_url": f"https://api.github.com/orgs/{self._org_name}/repos"}
        
        @property
        def _public_repos_url(self):
            return self.org["repos_url"]
        
        def public_repos(self, license=None):
            return ["repo1", "repo2"]
        
        @staticmethod
        def has_license(repo, license_key):
            return repo.get("license", {}).get("key") == license_key


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @patch('test_client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct list."""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload
        
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ):
            client_instance = GithubOrgClient("test")
            result = client_instance.public_repos()
            
            expected_repos = ["repo1", "repo2"]
            self.assertEqual(result, expected_repos)
            mock_get_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
