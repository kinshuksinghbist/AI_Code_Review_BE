import requests

def fetch_pr_details(repo_owner, repo_name, pr_number, github_token):
    """
    Fetch Pull Request details from GitHub API
    
    Args:
        repo_owner (str): GitHub repository owner
        repo_name (str): GitHub repository name
        pr_number (int): Pull Request number
        github_token (str): GitHub authentication token
    
    Returns:
        dict: Pull Request details including patch, title, body
    """
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3.patch'
    }
    
    pr_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}'
    patch_url = f'{pr_url}.patch'
    
    pr_response = requests.get(pr_url, headers=headers)
    patch_response = requests.get(patch_url, headers=headers)
    
    pr_details = pr_response.json()
    pr_details['patch'] = patch_response.text
    
    return pr_details
