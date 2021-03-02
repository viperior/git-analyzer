import json
from ratelimiter import RateLimiter
import requests

def get_config_value(key):
    with open('config.json', 'r') as config_file:
        config_json = json.load(config_file)

    return config_json[key]

def display_user_stats():
    user = get_user()

    print('Username: ', user['login'], '\nPublic repos: ', \
        user['public_repos'])

    repos = get_repos()

    for repo in repos:
        print('===')
        print('Repo: ', repo['name'])
        print('Branches: ')
        branches = get_branches(repo['branches_url'])

        for branch in branches:
            print('  ', branch['name'])

    return 0

def get_branches(branches_url):
    branch_list_url = branches_url.replace('{/branch}', '')
    branches = get_json(url=branch_list_url)
    return branches

@RateLimiter(max_calls=300, period=1800)
def get_json(url=False, endpoint=False):
    if url and (not endpoint):
        final_url = url
    elif (not url) and endpoint:
        base = 'https://api.github.com/'
        final_url = base + endpoint
    else:
        return False
    
    r = requests.get(final_url)
    return r.json()

def get_repos():
    username = get_config_value('username')
    repos = get_json(endpoint = 'users/' + username + '/repos')
    return repos

def get_user():
    username = get_config_value('username')
    return get_json(endpoint = 'users/' + username)

def main():
    display_user_stats()

main()
