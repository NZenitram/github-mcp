"""
Test module for GitHub repositories functionality.
"""
import os
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from src.tools.repositories import create_repo, update_repo_settings, get_github_client, delete_repo

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables before each test."""
    os.environ["GITHUB_TOKEN"] = "test_token"
    os.environ["GITHUB_USERNAME"] = "test_user"

@pytest.fixture
def mock_repo():
    """Create a mock repository."""
    mock_repo = MagicMock()
    mock_repo.name = "test-repo"
    mock_repo.full_name = "test_user/test-repo"
    mock_repo.description = "A test repository"
    mock_repo.private = False
    mock_repo.stargazers_count = 0
    mock_repo.forks_count = 0
    mock_repo.language = "Python"
    mock_repo.html_url = "https://github.com/test_user/test-repo"
    mock_repo.created_at = datetime.now()
    mock_repo.updated_at = datetime.now()
    return mock_repo

@pytest.fixture
def mock_github(mock_repo):
    """Create a mock GitHub client."""
    with patch('src.tools.repositories.Github') as mock_github:
        # Create mock user
        mock_user = MagicMock()
        
        # Configure repository creation
        def create_repo_mock(**kwargs):
            # Update mock repo with creation parameters
            mock_repo.name = kwargs.get('name', mock_repo.name)
            mock_repo.description = kwargs.get('description', mock_repo.description)
            mock_repo.private = kwargs.get('private', mock_repo.private)
            return mock_repo
            
        mock_user.create_repo = MagicMock(side_effect=create_repo_mock)
        
        # Create mock GitHub instance
        mock_github_instance = MagicMock()
        mock_github_instance.get_user.return_value = mock_user
        mock_github_instance.get_repo.return_value = mock_repo
        
        mock_github.return_value = mock_github_instance
        yield mock_github_instance

def test_create_repo_basic(mock_github, mock_repo):
    """Test creating a basic repository."""
    # Create a test repository
    repo = create_repo(
        name="test-repo",
        description="A test repository",
        private=False
    )
    
    # Verify repository data
    assert repo.name == "test-repo"
    assert repo.description == "A test repository"
    assert not repo.private
    assert repo.language == "Python"
    
    # Verify GitHub API was called correctly
    mock_github.get_user().create_repo.assert_called_once_with(
        name="test-repo",
        description="A test repository",
        private=False,
        auto_init=False,
        gitignore_template=None,
        license_template=None
    )

def test_create_repo_with_init(mock_github, mock_repo):
    """Test creating a repository with initialization."""
    # Create a test repository with initialization
    repo = create_repo(
        name="test-repo",
        description="A test repository",
        private=True,
        auto_init=True,
        gitignore_template="Python",
        license_template="MIT"
    )
    
    # Verify repository data
    assert repo.name == "test-repo"
    assert repo.description == "A test repository"
    assert repo.private
    assert repo.language == "Python"
    
    # Verify GitHub API was called correctly
    mock_github.get_user().create_repo.assert_called_once_with(
        name="test-repo",
        description="A test repository",
        private=True,
        auto_init=True,
        gitignore_template="Python",
        license_template="MIT"
    )

def test_create_repo_minimal(mock_github, mock_repo):
    """Test creating a repository with minimal parameters."""
    # Create a test repository with just a name
    repo = create_repo(name="test-repo")
    
    # Verify repository data
    assert repo.name == "test-repo"
    assert repo.description is None
    assert not repo.private
    assert repo.language == "Python"
    
    # Verify GitHub API was called correctly
    mock_github.get_user().create_repo.assert_called_once_with(
        name="test-repo",
        description=None,
        private=False,
        auto_init=False,
        gitignore_template=None,
        license_template=None
    )

def test_update_repo_settings_basic(mock_github, mock_repo):
    """Test updating basic repository settings."""
    # Update repository settings
    settings = {
        "description": "Updated description",
        "private": True,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": True,
        "has_downloads": False,
        "has_pages": True,
        "has_discussions": False,
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "allow_rebase_merge": False,
        "delete_branch_on_merge": True,
        "archived": False,
        "topics": ["python", "testing"]
    }
    
    update_repo_settings(
        owner="test_user",
        repo="test-repo",
        settings=settings
    )
    
    # Verify GitHub API was called correctly
    mock_repo.edit.assert_called_once_with(**settings)

def test_update_repo_settings_minimal(mock_github, mock_repo):
    """Test updating repository settings with minimal changes."""
    # Update repository settings
    settings = {
        "description": "New description"
    }
    
    update_repo_settings(
        owner="test_user",
        repo="test-repo",
        settings=settings
    )
    
    # Verify GitHub API was called correctly
    mock_repo.edit.assert_called_once_with(**settings)

def test_update_repo_settings_empty(mock_github, mock_repo):
    """Test updating repository settings with empty settings."""
    # Update repository settings
    settings = {}
    
    update_repo_settings(
        owner="test_user",
        repo="test-repo",
        settings=settings
    )
    
    # Verify GitHub API was called correctly
    mock_repo.edit.assert_called_once_with(**settings)

def test_delete_repo(mock_github, mock_repo):
    """Test deleting a repository."""
    # Delete the repository
    delete_repo(
        owner="test_user",
        repo="test-repo"
    )
    
    # Verify GitHub API was called correctly
    mock_repo.delete.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 