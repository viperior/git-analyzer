from github import Github
import json

def get_config_value(key):
    with open('config.json', 'r') as input_file:
        config_json = json.load(input_file)

    return config_json[key]

def main():
    g = Github(get_config_value('github_access_token'))

    for repo in g.get_user().get_repos():
        print(repo.name)

main()
