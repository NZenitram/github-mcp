"""
Issue and pull request related tools for GitHub MCP.
"""
from typing import List, Dict, Optional
from github import Github, Issue, PullRequest
import os

def get_github_client() -> Github:
    """Get an initialized GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    return Github(token)

def search_issues(
    query: str,
    state: str = "open",
    sort: str = "created",
    order: str = "desc",
    max_results: int = 10
) -> List[Dict]:
    """
    Search for GitHub issues across repositories.
    
    Args:
        query: Search query string
        state: Issue state (open, closed, all)
        sort: Sort field
        order: Sort order
        max_results: Maximum number of results
        
    Returns:
        List of issue information dictionaries
    """
    github = get_github_client()
    
    # Add state to query if not "all"
    if state != "all":
        query = f"{query} state:{state}"
    
    # Search for issues
    issues = github.search_issues(query, sort=sort, order=order)
    
    # Format results
    results = []
    for issue in issues[:max_results]:
        results.append({
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "state": issue.state,
            "closed": issue.state == "closed",
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "url": issue.html_url,
            "repository": issue.repository.full_name
        })
    
    return results

def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[str] = None
) -> Dict:
    """
    Create a new GitHub issue.
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: Issue title
        body: Issue description
        labels: List of labels to apply
        assignees: List of assignee usernames
        milestone: Milestone to associate with the issue
        
    Returns:
        Created issue information dictionary
    """
    github = get_github_client()
    repository = github.get_repo(f"{owner}/{repo}")
    
    # Create the issue
    issue = repository.create_issue(
        title=title,
        body=body,
        labels=labels or [],
        assignees=assignees or []
    )
    
    # Return formatted issue data
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "closed": issue.state == "closed",
        "labels": [label.name for label in issue.labels],
        "assignees": [assignee.login for assignee in issue.assignees],
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
        "url": issue.html_url,
        "repository": issue.repository.full_name
    }

def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[str] = None
) -> Dict:
    """
    Update an existing GitHub issue.
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        title: New issue title
        body: New issue description
        state: New issue state
        labels: New list of labels
        assignees: New list of assignees
        milestone: New milestone
        
    Returns:
        Updated issue information dictionary
    """
    github = get_github_client()
    repository = github.get_repo(f"{owner}/{repo}")
    issue = repository.get_issue(issue_number)
    
    # Update issue fields
    update_kwargs = {}
    if title is not None:
        update_kwargs["title"] = title
    if body is not None:
        update_kwargs["body"] = body
    if state is not None:
        update_kwargs["state"] = state
    
    issue.edit(**update_kwargs)
    
    # Update labels if specified
    if labels is not None:
        issue.set_labels(*labels)
    
    # Update assignees if specified
    if assignees is not None:
        issue.set_assignees(assignees)
    
    # Return formatted issue data
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "closed": issue.state == "closed",
        "labels": [label.name for label in issue.labels],
        "assignees": [assignee.login for assignee in issue.assignees],
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
        "url": issue.html_url,
        "repository": issue.repository.full_name
    }

def create_pull_request(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    head: str = None,
    base: str = "main",
    draft: bool = False,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[str] = None
) -> Dict:
    """
    Create a new pull request.
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: PR title
        body: PR description
        head: Source branch
        base: Target branch
        draft: Whether to create as draft PR
        labels: List of labels to apply
        assignees: List of assignee usernames
        milestone: Milestone to associate with the PR
        
    Returns:
        Created pull request information dictionary
    """
    github = get_github_client()
    repository = github.get_repo(f"{owner}/{repo}")
    
    # Create the pull request
    pr = repository.create_pull(
        title=title,
        body=body,
        head=head,
        base=base,
        draft=draft
    )
    
    # Add labels if specified
    if labels:
        pr.set_labels(*labels)
    
    # Add assignees if specified
    if assignees:
        pr.add_to_assignees(*assignees)
    
    # Return formatted PR data
    return {
        "number": pr.number,
        "title": pr.title,
        "body": pr.body,
        "state": pr.state,
        "draft": pr.draft,
        "labels": [label.name for label in pr.labels],
        "assignees": [assignee.login for assignee in pr.assignees],
        "created_at": pr.created_at.isoformat(),
        "updated_at": pr.updated_at.isoformat(),
        "url": pr.html_url,
        "repository": pr.repository.full_name,
        "head": pr.head.ref,
        "base": pr.base.ref
    }

def manage_issue_labels(
    owner: str,
    repo: str,
    issue_number: int,
    labels: List[str]
) -> None:
    """
    Manage issue labels.
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        labels: List of labels to set
    """
    # Implementation will be added later
    pass 