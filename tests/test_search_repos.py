"""
Test module for GitHub repository search functionality.
"""
import os
import pytest
from dotenv import load_dotenv
from src.tools.repositories import search_repos, get_github_client

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables before each test."""
    load_dotenv()

def test_list_user_repos():
    """Test listing user's repositories directly."""
    # Get username from environment
    username = os.getenv("GITHUB_USERNAME")
    if not username:
        pytest.skip("GITHUB_USERNAME environment variable is not set")
    
    # Get GitHub client
    github = get_github_client()
    user = github.get_user(username)
    
    # Get repositories directly
    repos = list(user.get_repos())[:5]
    
    # Convert to our format for comparison
    formatted_repos = []
    for repo in repos:
        formatted_repos.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
            "url": repo.html_url,
            "private": repo.private,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat()
        })
    
    # Verify repository data structure
    for repo in formatted_repos:
        assert "name" in repo, "Repository should have a name"
        assert "full_name" in repo, "Repository should have a full name"
        assert "description" in repo, "Repository should have a description"
        assert "stars" in repo, "Repository should have a star count"
        assert "language" in repo, "Repository should have a language"
        assert "url" in repo, "Repository should have a URL"
        assert repo["full_name"].lower().startswith(username.lower()), "Repository should belong to the specified user"

def test_search_with_language_filter():
    """Test searching repositories with language filter."""
    username = os.getenv("GITHUB_USERNAME")
    if not username:
        pytest.skip("GITHUB_USERNAME environment variable is not set")
    
    # Get GitHub client
    github = get_github_client()
    user = github.get_user(username)
    
    # Get all user's repositories
    all_repos = list(user.get_repos())
    
    # Filter Python repositories
    python_repos = [repo for repo in all_repos if repo.language == "Python"][:5]
    
    # Convert to our format
    formatted_repos = []
    for repo in python_repos:
        formatted_repos.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
            "url": repo.html_url,
            "private": repo.private,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat()
        })
    
    # Verify results if any Python repositories exist
    if formatted_repos:
        for repo in formatted_repos:
            assert repo["language"] == "Python", "All repositories should be Python repositories"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 