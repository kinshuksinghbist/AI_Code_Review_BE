import requests

def fetch_pr_details(repo_owner, repo_name, pr_number, github_token):
    headers = {
        'Authorization': f'token {github_token}',
    }
    
    pr_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}'
    patch_url = f'https://github.com/{repo_owner}/{repo_name}/pull/{pr_number}.diff'
    
    pr_response = requests.get(pr_url, headers=headers)
    patch_response = requests.get(patch_url, headers=headers)

    pr_details = pr_response.json()
    pr_details['patch'] = patch_response.text
    pr_details['number'] = pr_number
    
    return pr_details
