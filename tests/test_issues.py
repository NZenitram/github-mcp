"""
Test module for GitHub issues functionality.
"""
import os
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from src.tools.issues import create_issue, update_issue, search_issues, get_github_client

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables before each test."""
    os.environ["GITHUB_TOKEN"] = "test_token"
    os.environ["GITHUB_USERNAME"] = "test_user"

@pytest.fixture
def mock_issue():
    """Create a mock issue."""
    # Create mock repository
    mock_repo = MagicMock()
    mock_repo.full_name = "test_user/test_repo"
    
    # Create mock label and assignee
    mock_label = MagicMock()
    mock_label.name = "test"
    mock_assignee = MagicMock()
    mock_assignee.login = "test_user"
    
    # Create mock issue
    mock_issue = MagicMock()
    mock_issue.number = 1
    mock_issue.title = "Test Issue"
    mock_issue.body = "Test Body"
    mock_issue.state = "open"
    mock_issue.labels = [mock_label]
    mock_issue.assignees = [mock_assignee]
    mock_issue.created_at = datetime.now()
    mock_issue.updated_at = datetime.now()
    mock_issue.html_url = "https://github.com/test_user/test_repo/issues/1"
    mock_issue.repository = mock_repo
    
    # Configure issue methods
    def edit_mock(**kwargs):
        if 'title' in kwargs:
            mock_issue.title = kwargs['title']
        if 'body' in kwargs:
            mock_issue.body = kwargs['body']
        if 'state' in kwargs:
            mock_issue.state = kwargs['state']
            mock_issue.closed = kwargs['state'] == 'closed'
    
    mock_issue.edit = MagicMock(side_effect=edit_mock)
    
    return mock_issue

@pytest.fixture
def mock_github(mock_issue):
    """Create a mock GitHub client."""
    with patch('src.tools.issues.Github') as mock_github:
        # Create mock repository
        mock_repo = MagicMock()
        mock_repo.full_name = "test_user/test_repo"
        mock_repo.get_issue.return_value = mock_issue
        
        # Configure repository methods to return our mock issue
        def create_issue_mock(**kwargs):
            if 'title' in kwargs:
                mock_issue.title = kwargs['title']
            if 'body' in kwargs:
                mock_issue.body = kwargs['body']
            if 'labels' in kwargs:
                mock_label = MagicMock()
                mock_label.name = kwargs['labels'][0]
                mock_issue.labels = [mock_label]
            return mock_issue
            
        mock_repo.create_issue = MagicMock(side_effect=create_issue_mock)
        
        # Create mock user
        mock_user = MagicMock()
        mock_user.get_repo.return_value = mock_repo
        
        # Create mock GitHub instance
        mock_github_instance = MagicMock()
        mock_github_instance.get_user.return_value = mock_user
        mock_github_instance.get_repo.return_value = mock_repo
        mock_github_instance.search_issues.return_value = [mock_issue]
        
        mock_github.return_value = mock_github_instance
        yield mock_github_instance

def test_create_issue(mock_github, mock_issue):
    """Test creating a new issue."""
    # Create a test issue
    issue = create_issue(
        owner="test_user",
        repo="test_repo",
        title="New Issue",
        body="This is a test issue created by automated tests",
        labels=["test", "automated"],
    )
    
    # Verify issue data
    assert issue["title"] == "New Issue"
    assert issue["body"] == "This is a test issue created by automated tests"
    assert "test" in issue["labels"]
    assert not issue["closed"]
    assert issue["number"] == 1
    
    # Verify GitHub API was called correctly
    mock_github.get_user().get_repo().create_issue.assert_called_with(
        title="New Issue",
        body="This is a test issue created by automated tests",
        labels=["test", "automated"],
        assignees=[]
    )

def test_update_issue(mock_github, mock_issue):
    """Test updating an existing issue."""
    # Update the issue
    updated_issue = update_issue(
        owner="test_user",
        repo="test_repo",
        issue_number=1,
        title="Updated Title",
        body="This issue has been updated",
        state="closed",
    )
    
    # Verify updates
    assert updated_issue["title"] == "Updated Title"
    assert updated_issue["body"] == "This issue has been updated"
    assert updated_issue["closed"]
    assert updated_issue["number"] == 1
    
    # Verify GitHub API was called correctly
    mock_issue.edit.assert_called_once_with(
        title="Updated Title",
        body="This issue has been updated",
        state="closed"
    )

def test_search_issues(mock_github):
    """Test searching for issues."""
    # Search for issues
    results = search_issues(
        query="repo:test_user/test_repo label:bug",
        state="open"
    )
    
    # Verify search results
    assert len(results) == 1
    assert results[0]["title"] == "Test Issue"
    assert "test" in results[0]["labels"]
    
    # Verify GitHub API was called correctly
    mock_github.search_issues.assert_called_once_with(
        "repo:test_user/test_repo label:bug state:open",
        sort="created",
        order="desc"
    )

def test_issue_labels(mock_github, mock_issue):
    """Test issue label management."""
    # Update issue labels
    updated_issue = update_issue(
        owner="test_user",
        repo="test_repo",
        issue_number=1,
        labels=["new-label", "another-label"],
    )
    
    # Verify labels
    assert "test" in updated_issue["labels"]
    
    # Verify GitHub API was called correctly
    mock_issue.set_labels.assert_called_once_with(
        "new-label", "another-label"
    )

if __name__ == "__main__":
    pytest.main([__file__, "-v"])