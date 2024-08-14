#! /usr/bin/env python3

import argparse
import requests

from github import Auth, Github, GithubException
from tqdm import tqdm
from utils import get_github_token, get_organization_repositories, get_direct_members


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--organization', help='The name of the GitHub organization to audit',
                        default='opendatahub-io')
    return parser.parse_args()


def requests_get(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request('GET', url, headers=headers)

    assert(response.status_code == 200)
    return response.json()


def get_repository_rulesets(token, repo):
    url = f'https://api.github.com/repos/{repo}/rulesets'
    return requests_get(token, url)


def get_rule(token, rule_url):
    return requests_get(token, rule_url)


def rule_matches_requirement(rule):
    protects_default_branch = False
    requires_pull_request = False
    
    conditions_includes = rule.get('conditions', {}).get('ref_name', {}).get('include', [])
    if '~DEFAULT_BRANCH' in conditions_includes:
        protects_default_branch = True

    rules = rule.get('rules', [])
    rule_types = set((r.get('type', '') for r in rules))
    requires_pull_request = 'pull_request' in rule_types

    return protects_default_branch and requires_pull_request
    

def main():
    args = parse_args()
    github_token = get_github_token()
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    repos = get_organization_repositories(g, args.organization)

    print(f'Checking for repositories without branch protection rules in place for the default branch...')
    for repo in tqdm(repos):
        rulesets = get_repository_rulesets(github_token, repo)
        rule_found = False
        for rule in rulesets:
            if rule.get('target', '') == 'branch' and rule.get('enforcement', '') == 'active':
                rule_url = rule['_links']['self']['href']
                rule_details = get_rule(github_token, rule_url)
                if rule_matches_requirement(rule_details):
                    rule_found = True
                    break
        if not rule_found:
            tqdm.write(f'Repository {repo} does not have a rule requiring pull requests for the default branch!')


if __name__ == '__main__':
    main()