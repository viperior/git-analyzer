import json
from ratelimiter import RateLimiter
import requests

def get_config_value(key):
    with open('config.json', 'r') as config_file:
        config_json = json.load(config_file)

    return config_json[key]

def display_user_stats():
    with open('data/out.txt', 'a') as output_file:
        dashes = '==='
        user = get_user()
        print('user ==== ', user)
        write_line_to_file(dashes, output_file, True)
        write_line_to_file(
            'Username: ' + user['login'] + '\nPublic repos: ' + \
            str(user['public_repos']), 
            output_file, 
            True
        )
        write_line_to_file(dashes, output_file, True)
        repos = get_repos()

        for repo in repos:
            write_line_to_file(dashes, output_file, True)
            write_line_to_file('Repo: ' + repo['name'], output_file, True)
            write_line_to_file('Branches: ', output_file, True)
            branches = get_branches(repo['branches_url'])

            for branch in branches:
                write_line_to_file(' ' + branch['name'], output_file, True)

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

def write_line_to_file(line_text, file, print_line_text=False):
    if print_line_text:
        print(line_text)

    file.write(line_text + '\n')

def main():
    display_user_stats()

main()
