from get_config_value import get_config_value
from github import Github
import json
from ratelimiter import RateLimiter
from time import gmtime, strftime

def get_user_repo_branches():
    extract_json = {
        'data_source_access_time': strftime("%Y%m%dT%H%M%SZ", gmtime()),
        'data_source_name': 'GitHub API'
    }
    g = Github(get_config_value('github_access_token'))
    user = g.get_user()
    user_json = {
        'login': user.login,
        'public_repos': user.public_repos,
        'repos': {}
    }
    repos = user.get_repos()

    for i, repo in enumerate(repos):
        if i >= get_config_value('max_repos_to_download'):
            pass
        else:
            repo_name = repo.name
            repo_json = {
                'name': repo_name,
                'private': repo.private,
                'forks_count': repo.forks_count,
                'stargazers_count': repo.stargazers_count,
                'watchers_count': repo.watchers_count,
                'size': repo.size,
                'open_issues_count': repo.open_issues_count,
                'has_issues': repo.has_issues,
                'has_projects': repo.has_projects,
                'has_wiki': repo.has_wiki,
                'has_downloads': repo.has_downloads,
                'pushed_at': repo.pushed_at,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'branches': {}
            }
            branches = repo.get_branches()

            for branch in branches:
                branch_name = branch.name
                branch_commit = branch.commit
                branch_json = {
                    'name': branch_name,
                    'commit': {
                        'sha': branch_commit.sha,
                        'url': branch_commit.url
                    },
                    'protected': branch.protected,
                }
                repo_json['branches'][branch_name] = branch_json

        user_json['repos'][repo_name] = repo_json

    extract_json['data'] = user_json

    with open('data/user_repo_branches.json', 'w') as output_file:
        json.dump(extract_json, output_file, indent=4, default=str)

def display_rate_limit():
    g = Github(get_config_value('github_access_token'))
    print('Rate limit stats:\nCore limit: ', g.rate_limiting[0])

def prompt_user_to_continue():
    user_input = input('Do you wish to proceed? (y/n): ')
    return user_input.upper() == 'Y'

def main():
    display_rate_limit()

    if prompt_user_to_continue():
        get_user_repo_branches()

main()
