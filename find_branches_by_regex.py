from get_config_value import get_config_value
import json
import re

def main():
    with open('data/user_repo_branches.json', 'r') as input_file:
        json_data = json.load(input_file)

    print('Data source access time: ', json_data['data_source_access_time'])

    for repo_key in json_data['data']['repos']:
        repo = json_data['data']['repos'][repo_key]
        
        for branch_key in repo['branches']:
            branch = repo['branches'][branch_key]
            match = re.search(get_config_value('branch_search_pattern'), 
                branch['name'])
            
            if match:
                print('Matching branch found in ', repo['name'], ':', 
                    branch['name'])

main()
