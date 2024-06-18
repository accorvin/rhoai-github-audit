import os


def get_github_token():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_file_path = os.path.join(dir_path, '.github_token')
    if not os.path.exists(token_file_path):
        print(f'You must create your GitHub token file at {token_file_path}')
        exit(1)
    with open(token_file_path) as f:
        return f.read().strip()
    

def get_organization_repositories(github_client, org_name):
    org = github_client.get_organization(org_name)
    org_repos = org.get_repos()
    return [repo.full_name for repo in org_repos]


def get_direct_members(github_client, repo_name):
    repo_obj = github_client.get_repo(repo_name)
    collaborators = repo_obj.get_collaborators(affiliation='direct')
    res = [c.login for c in collaborators]
    return res