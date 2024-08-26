#! /usr/bin/env python3

import argparse

from github import Auth, Github
from tqdm import tqdm
from utils import get_github_token, get_organization_repositories, get_direct_members

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--organization', help='The name of the GitHub organization to audit',
                        default='opendatahub-io')
    parser.add_argument('-e', action='store_true', default=False,
                        dest='use_env',
                        help='Use GITHUB_TOKEN env var instead of file')
    return parser.parse_args()

def main():
    args = parse_args()
    github_token = get_github_token(use_env=args.use_env)
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    repos = get_organization_repositories(g, args.organization)

    print(f'Checking for repositories with users added directly...')
    direct_membership_exists = False
    for repo in tqdm(repos):
        direct_members = get_direct_members(g, repo)
        if direct_members:
            direct_membership_exists = True
            tqdm.write(f'Repo {repo} has individuals added directly instead of via a team!')
            for m in direct_members:
                tqdm.write(f'\t{m}')
    if direct_membership_exists:
        exit(1)


if __name__ == '__main__':
    main()