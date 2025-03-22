# GitHub MCP Tools

A Multi-Claude Program (MCP) for interacting with GitHub APIs through Claude Desktop.

## Features

- Search GitHub repositories and issues
- Create, update, and manage GitHub issues and pull requests
- Manage repository settings and configurations
- Handle repository workflows and actions
- Search for users and organizations
- Manage repository collaborators and teams

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/github-mcp.git
   cd github-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

5. Add your GitHub credentials to the `.env` file:
   ```
   GITHUB_TOKEN=your_personal_access_token_here
   GITHUB_USERNAME=your_github_username
   ```

6. Test the installation:
   ```bash
   # Run all tests
   python -m pytest

   # Run a specific test file
   python -m pytest tests/test_search_repos.py
   ```

7. Start the MCP server:
   ```bash
   python run.py
   ```

## Environment Setup

### GitHub Personal Access Token
You'll need a fine-grained personal access token to authenticate with GitHub:

1. Log in to your GitHub account
2. Go to Settings > Developer settings > Personal access tokens > Fine-grained tokens
3. Click "Generate new token"
4. Configure the token:
   - Token name: "Claude Desktop Integration"
   - Description: "Token for Claude Desktop GitHub integration"
   - Expiration: Choose an appropriate expiration date
   - Repository access: Select "All repositories" or specific repositories
   - Permissions:
     - Repository permissions:
       - Actions: Read and write
       - Contents: Read and write
       - Issues: Read and write
       - Pull requests: Read and write
       - Repository hooks: Read and write
       - Repository settings: Read and write
     - Organization permissions (if working with organization repositories):
       - Members: Read-only
       - Teams: Read-only
5. Click "Generate token" and save the generated token securely

## Tools

### Search Repositories
Search for GitHub repositories using various criteria.

**Parameters:**
- query: Search query string
- sort: Sort field (stars, forks, updated, etc.)
- order: Sort order (asc or desc)
- max_results: Maximum number of results to return (default: 10)

### Create Issue
Create a new GitHub issue in a specified repository.

**Parameters:**
- owner: Repository owner
- repo: Repository name
- title: Issue title
- body: Issue description
- labels: List of labels to apply
- assignees: List of assignee usernames

### Create Pull Request
Create a new pull request.

**Parameters:**
- owner: Repository owner
- repo: Repository name
- title: PR title
- body: PR description
- head: Source branch
- base: Target branch
- draft: Whether to create as draft PR

### Manage Repository Settings
Update repository settings and configurations.

**Parameters:**
- owner: Repository owner
- repo: Repository name
- settings: Dictionary of settings to update

### Search Issues
Search for issues across repositories.

**Parameters:**
- query: Search query string
- state: Issue state (open, closed, all)
- sort: Sort field
- order: Sort order
- max_results: Maximum number of results

### Manage Workflows
Manage GitHub Actions workflows.

**Parameters:**
- owner: Repository owner
- repo: Repository name
- workflow_file: Workflow file path
- action: Action to perform (enable, disable, trigger)

### Manage Collaborators
Manage repository collaborators.

**Parameters:**
- owner: Repository owner
- repo: Repository name
- username: Collaborator username
- permission: Permission level (pull, push, admin, maintain, triage)

## Example Usage

```python
# Search for repositories
search_repos(query="python web framework", sort="stars", max_results=5)

# Create a new issue
create_issue(
    owner="username",
    repo="repository",
    title="Bug: Login not working",
    body="Users cannot log in using the login button",
    labels=["bug", "high-priority"]
)

# Create a pull request
create_pull_request(
    owner="username",
    repo="repository",
    title="Feature: Add user authentication",
    body="Implements JWT-based authentication",
    head="feature/auth",
    base="main"
)

# Search for issues
search_issues(query="is:open is:issue author:username", max_results=10)

# Manage repository settings
manage_repo_settings(
    owner="username",
    repo="repository",
    settings={
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
)
```

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_search_repos.py
```

### Adding New Tools
1. Create a new file in `src/tools/`
2. Implement your tool function
3. Register the tool in `src/main.py`
4. Add tests in `tests/`
5. Update documentation in README.md

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License
MIT License 