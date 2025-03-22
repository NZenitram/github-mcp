#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from github import Github

# Load environment variables from .env file
load_dotenv()

def initialize_github():
    """Initialize and return GitHub client connection using environment variables."""
    github_token = os.getenv("GITHUB_TOKEN")
    github_username = os.getenv("GITHUB_USERNAME")
    
    if not all([github_token, github_username]):
        raise ValueError("Missing required GitHub environment variables")
    
    github = Github(github_token)
    return github

def main():
    # Initialize GitHub connection
    github_client = initialize_github()
    
    # Initialize FastMCP
    app = FastMCP(name="github-tools")
    
    # Import tools
    from src.tools.repositories import (
        search_repos, create_repo, update_repo_settings,
        manage_collaborators, manage_workflows
    )
    from src.tools.issues import (
        search_issues, create_issue, update_issue,
        create_pull_request, manage_issue_labels
    )
    
    # Register tools using the add_tool method
    app.add_tool(
        search_repos,
        name="search_repos",
        description="Search for GitHub repositories using various criteria"
    )
    
    app.add_tool(
        create_repo,
        name="create_repo",
        description="Create a new GitHub repository"
    )
    
    app.add_tool(
        update_repo_settings,
        name="update_repo_settings",
        description="Update repository settings and configurations"
    )
    
    app.add_tool(
        manage_collaborators,
        name="manage_collaborators",
        description="Manage repository collaborators"
    )
    
    app.add_tool(
        manage_workflows,
        name="manage_workflows",
        description="Manage GitHub Actions workflows"
    )
    
    app.add_tool(
        search_issues,
        name="search_issues",
        description="Search for GitHub issues across repositories"
    )
    
    app.add_tool(
        create_issue,
        name="create_issue",
        description="Create a new GitHub issue"
    )
    
    app.add_tool(
        update_issue,
        name="update_issue",
        description="Update an existing GitHub issue"
    )
    
    app.add_tool(
        create_pull_request,
        name="create_pull_request",
        description="Create a new pull request"
    )
    
    app.add_tool(
        manage_issue_labels,
        name="manage_issue_labels",
        description="Manage issue labels"
    )
    
    # Start the FastMCP application
    app.run()

if __name__ == "__main__":
    main() 