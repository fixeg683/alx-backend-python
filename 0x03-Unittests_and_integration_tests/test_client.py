#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    # ... other test methods ...

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct list."""
        # Mock the payload for get_json
        test_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_repos
        
        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url',
                         new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            
            client = GithubOrgClient("test")
            result = client.public_repos()
            
            # Assert the result is correct
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            
            # Assert mocks were called correctly
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")


if __name__ == '__main__':
    unittest.main()
