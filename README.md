# RHOAI GitHub Audit

We use this repository to audit the Open Data Hub and Red Hat Data Services
GitHub organizations in order to find places where the active permissions,
branch protection rules, etc. do not match our desired standards.

## Usage

### Setup

#### GitHub Access Token

These scripts all rely on a GitHub personal access token existing in a file
called `.github_token`. This file should be saved at the root of this repository
in your local filesystem and should _not_ be stored in Git.

Follow the instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) to create
a GitHub personal access token (classic). When creating the token, give it all `repo` permissions as well as `read:org` permissions.

#### Python Dependencies

We use Pipenv to install various python packages required to run these scripts. Install Pipenv by following the instructions [here](https://pipenv.pypa.io/en/latest/installation.html). Then run the following commands from the root of this
repository to create the pipenv environment and install the required packages:

```
pipenv shell
pipenv install
```

### Scripts

#### Find Repositories with users added directly

We want to use GitHub teams to manage access to repositories rather than adding 
individuals directly to a repository. To generate a list of all repositories in
violation of this policy, run the following script:
```
python list_repos_with_direct_members.py
```

#### Find repositories without branch protection rules

We want all repositories to have a ruleset in place requiring pull requests to
the default branch. To generate a list of all repositories in violation of
this policy, run the following script:
```
python list_repos_without_branch_protection.py
```