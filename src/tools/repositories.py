"""
Repository-related tools for GitHub MCP.
"""
from typing import List, Dict, Optional
from github import Github, Repository
import os

def get_github_client() -> Github:
    """Get an initialized GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    return Github(token)

def search_repos(
    query: str = "",
    sort: str = "updated",
    order: str = "desc",
    max_results: int = 10,
    user: Optional[str] = None
) -> List[Dict]:
    """
    List GitHub repositories with optional filtering.
    
    Args:
        query: Optional filter string (e.g., "language:python")
        sort: Sort field (updated, created, pushed)
        order: Sort order (asc or desc)
        max_results: Maximum number of results to return
        user: Optional username to list repositories for
        
    Returns:
        List of repository information dictionaries
    """
    github = get_github_client()
    
    # Get user's repositories
    if user:
        user_obj = github.get_user(user)
        repos = list(user_obj.get_repos())
    else:
        # If no user specified, get authenticated user's repos
        user_obj = github.get_user()
        repos = list(user_obj.get_repos())
    
    # Apply language filter if specified
    if query.startswith("language:"):
        language = query.split(":")[1]
        repos = [repo for repo in repos if repo.language and repo.language.lower() == language.lower()]
    
    # Sort repositories
    if sort == "updated":
        repos.sort(key=lambda x: x.updated_at, reverse=(order == "desc"))
    elif sort == "created":
        repos.sort(key=lambda x: x.created_at, reverse=(order == "desc"))
    elif sort == "stars":
        repos.sort(key=lambda x: x.stargazers_count, reverse=(order == "desc"))
    
    # Format results
    results = []
    for repo in repos[:max_results]:
        results.append({
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
    
    return results

def create_repo(
    name: str,
    description: Optional[str] = None,
    private: bool = False,
    auto_init: bool = False,
    gitignore_template: Optional[str] = None,
    license_template: Optional[str] = None
) -> Repository:
    """
    Create a new GitHub repository.
    
    Args:
        name: Repository name
        description: Repository description
        private: Whether the repository should be private
        auto_init: Whether to initialize with README
        gitignore_template: Gitignore template to use
        license_template: License template to use
        
    Returns:
        Created repository object
    """
    github = get_github_client()
    user = github.get_user()
    
    # Create the repository
    repo = user.create_repo(
        name=name,
        description=description,
        private=private,
        auto_init=auto_init,
        gitignore_template=gitignore_template,
        license_template=license_template
    )
    
    return repo

def update_repo_settings(
    owner: str,
    repo: str,
    settings: Dict
) -> None:
    """
    Update repository settings and configurations.
    
    Args:
        owner: Repository owner
        repo: Repository name
        settings: Dictionary of settings to update. Can include:
            - description: Repository description
            - private: Whether the repository is private
            - has_issues: Whether issues are enabled
            - has_projects: Whether projects are enabled
            - has_wiki: Whether wiki is enabled
            - has_downloads: Whether downloads are enabled
            - has_pages: Whether pages are enabled
            - has_discussions: Whether discussions are enabled
            - allow_squash_merge: Whether squash merging is allowed
            - allow_merge_commit: Whether merge commits are allowed
            - allow_rebase_merge: Whether rebase merging is allowed
            - delete_branch_on_merge: Whether to delete branches after merging
            - archived: Whether the repository is archived
            - topics: List of repository topics
    """
    github = get_github_client()
    repository = github.get_repo(f"{owner}/{repo}")
    
    # Update repository settings
    repository.edit(**settings)

def manage_collaborators(
    owner: str,
    repo: str,
    username: str,
    permission: str = "push"
) -> None:
    """
    Manage repository collaborators.
    
    Args:
        owner: Repository owner
        repo: Repository name
        username: Collaborator username
        permission: Permission level (pull, push, admin, maintain, triage)
    """
    # Implementation will be added later
    pass

def manage_workflows(
    owner: str,
    repo: str,
    workflow_file: str,
    action: str
) -> None:
    """
    Manage GitHub Actions workflows.
    
    Args:
        owner: Repository owner
        repo: Repository name
        workflow_file: Workflow file path
        action: Action to perform (enable, disable, trigger)
    """
    # Implementation will be added later
    pass 