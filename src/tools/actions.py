"""
GitHub Actions API wrapper for workflow management.
"""
from typing import Dict, List, Optional
from github import Github
import os

class GitHubActions:
    """Wrapper for GitHub Actions API functionality."""
    
    def __init__(self, github_client: Github):
        """
        Initialize the GitHub Actions wrapper.
        
        Args:
            github_client: Initialized GitHub client
        """
        self.github = github_client

    def list_workflows(self, owner: str, repo: str) -> List[Dict]:
        """
        List all workflows in a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of workflow information dictionaries containing:
                - id: Workflow ID
                - name: Workflow name
                - path: Path to workflow file
                - state: Workflow state (active/inactive)
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
        """
        repository = self.github.get_repo(f"{owner}/{repo}")
        workflows = repository.get_workflows()
        return [{
            "id": w.id,
            "name": w.name,
            "path": w.path,
            "state": w.state,
            "created_at": w.created_at,
            "updated_at": w.updated_at
        } for w in workflows]

    def get_workflow(self, owner: str, repo: str, workflow_id: int) -> Dict:
        """
        Get details of a specific workflow.
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID
            
        Returns:
            Dictionary containing workflow information:
                - id: Workflow ID
                - name: Workflow name
                - path: Path to workflow file
                - state: Workflow state
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
        """
        repository = self.github.get_repo(f"{owner}/{repo}")
        workflow = repository.get_workflow(workflow_id)
        return {
            "id": workflow.id,
            "name": workflow.name,
            "path": workflow.path,
            "state": workflow.state,
            "created_at": workflow.created_at,
            "updated_at": workflow.updated_at
        }

    def list_workflow_runs(
        self,
        owner: str,
        repo: str,
        workflow_id: int,
        status: Optional[str] = None,
        branch: Optional[str] = None
    ) -> List[Dict]:
        """
        List runs of a specific workflow.
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID
            status: Filter by status (queued, in_progress, completed, etc.)
            branch: Filter by branch name
            
        Returns:
            List of workflow run information dictionaries containing:
                - id: Run ID
                - status: Run status
                - conclusion: Run conclusion (success/failure)
                - head_branch: Branch the run was executed on
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
        """
        repository = self.github.get_repo(f"{owner}/{repo}")
        workflow = repository.get_workflow(workflow_id)
        runs = workflow.runs()
        
        if status:
            runs = [r for r in runs if r.status == status]
        if branch:
            runs = [r for r in runs if r.head_branch == branch]
            
        return [{
            "id": r.id,
            "status": r.status,
            "conclusion": r.conclusion,
            "head_branch": r.head_branch,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        } for r in runs]

    def dispatch_workflow(
        self,
        owner: str,
        repo: str,
        workflow_id: int,
        ref: str,
        inputs: Optional[Dict] = None
    ) -> Dict:
        """
        Manually trigger a workflow run.
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID
            ref: Branch or commit to run the workflow on
            inputs: Optional workflow inputs
            
        Returns:
            Dictionary containing information about the triggered run:
                - id: Run ID
                - status: Initial run status
                - head_branch: Branch the run was executed on
                - created_at: Creation timestamp
        """
        repository = self.github.get_repo(f"{owner}/{repo}")
        workflow = repository.get_workflow(workflow_id)
        
        # Create workflow dispatch event
        workflow.create_dispatch(ref, inputs or {})
        
        # Get the latest run
        runs = list(workflow.runs())
        latest_run = runs[0] if runs else None
        
        if not latest_run:
            raise ValueError("No workflow runs found")
            
        return {
            "id": latest_run.id,
            "status": latest_run.status,
            "head_branch": latest_run.head_branch,
            "created_at": latest_run.created_at
        }

    def set_workflow_permissions(
        self,
        owner: str,
        repo: str,
        workflow_id: int,
        permissions: Dict[str, str]
    ) -> None:
        """
        Set permissions for a workflow.
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID
            permissions: Dictionary of permissions to set
                (e.g., {"actions": "write", "contents": "read"})
                
        Note:
            Available permissions:
                - actions: read/write
                - contents: read/write
                - metadata: read
        """
        repository = self.github.get_repo(f"{owner}/{repo}")
        workflow = repository.get_workflow(workflow_id)
        workflow.set_permissions(permissions) 