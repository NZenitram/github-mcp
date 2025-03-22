"""
Test module for GitHub Actions API wrapper.
"""
import os
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from src.tools.actions import GitHubActions

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables before each test."""
    os.environ["GITHUB_TOKEN"] = "test_token"
    os.environ["GITHUB_USERNAME"] = "test_user"

@pytest.fixture
def mock_workflow():
    """Create a mock workflow."""
    mock_workflow = MagicMock()
    mock_workflow.id = 123
    mock_workflow.name = "Test Workflow"
    mock_workflow.path = ".github/workflows/test.yml"
    mock_workflow.state = "active"
    mock_workflow.created_at = datetime.now()
    mock_workflow.updated_at = datetime.now()
    return mock_workflow

@pytest.fixture
def mock_workflow_run():
    """Create a mock workflow run."""
    mock_run = MagicMock()
    mock_run.id = 456
    mock_run.status = "completed"
    mock_run.conclusion = "success"
    mock_run.head_branch = "main"
    mock_run.created_at = datetime.now()
    mock_run.updated_at = datetime.now()
    return mock_run

@pytest.fixture
def mock_github(mock_workflow, mock_workflow_run):
    """Create a mock GitHub client."""
    with patch('src.tools.actions.Github') as mock_github:
        # Create mock repository
        mock_repo = MagicMock()
        
        # Configure workflow methods
        mock_repo.get_workflows.return_value = [mock_workflow]
        mock_repo.get_workflow.return_value = mock_workflow
        
        # Configure workflow run methods
        mock_workflow.runs.return_value = [mock_workflow_run]
        mock_workflow.create_dispatch.return_value = None
        
        # Create mock GitHub instance
        mock_github_instance = MagicMock()
        mock_github_instance.get_repo.return_value = mock_repo
        
        mock_github.return_value = mock_github_instance
        yield mock_github_instance

@pytest.fixture
def actions_client(mock_github):
    """Create a GitHubActions client."""
    return GitHubActions(mock_github)

def test_list_workflows(actions_client, mock_workflow):
    """Test listing workflows in a repository."""
    workflows = actions_client.list_workflows("test_user", "test-repo")
    
    assert len(workflows) == 1
    assert workflows[0]["id"] == mock_workflow.id
    assert workflows[0]["name"] == mock_workflow.name
    assert workflows[0]["path"] == mock_workflow.path
    assert workflows[0]["state"] == mock_workflow.state

def test_get_workflow(actions_client, mock_workflow):
    """Test getting a specific workflow."""
    workflow = actions_client.get_workflow("test_user", "test-repo", 123)
    
    assert workflow["id"] == mock_workflow.id
    assert workflow["name"] == mock_workflow.name
    assert workflow["path"] == mock_workflow.path
    assert workflow["state"] == mock_workflow.state

def test_list_workflow_runs(actions_client, mock_workflow_run):
    """Test listing workflow runs."""
    runs = actions_client.list_workflow_runs("test_user", "test-repo", 123)
    
    assert len(runs) == 1
    assert runs[0]["id"] == mock_workflow_run.id
    assert runs[0]["status"] == mock_workflow_run.status
    assert runs[0]["conclusion"] == mock_workflow_run.conclusion
    assert runs[0]["head_branch"] == mock_workflow_run.head_branch

def test_list_workflow_runs_with_filters(actions_client, mock_workflow_run):
    """Test listing workflow runs with filters."""
    # Test status filter
    runs = actions_client.list_workflow_runs(
        "test_user", "test-repo", 123, status="completed"
    )
    assert len(runs) == 1
    assert runs[0]["status"] == "completed"
    
    # Test branch filter
    runs = actions_client.list_workflow_runs(
        "test_user", "test-repo", 123, branch="main"
    )
    assert len(runs) == 1
    assert runs[0]["head_branch"] == "main"

def test_dispatch_workflow(actions_client, mock_workflow_run):
    """Test manually triggering a workflow."""
    result = actions_client.dispatch_workflow(
        "test_user",
        "test-repo",
        123,
        "main",
        {"input1": "value1"}
    )
    
    assert result["id"] == mock_workflow_run.id
    assert result["status"] == mock_workflow_run.status
    assert result["head_branch"] == mock_workflow_run.head_branch

def test_set_workflow_permissions(actions_client, mock_workflow):
    """Test setting workflow permissions."""
    permissions = {
        "actions": "write",
        "contents": "read"
    }
    
    actions_client.set_workflow_permissions(
        "test_user",
        "test-repo",
        123,
        permissions
    )
    
    mock_workflow.set_permissions.assert_called_once_with(permissions)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 