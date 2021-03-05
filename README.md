# git-analyzer
Analyze the repositories and branches of a GitHub user

## Configure
### config.json
```
{
    "username": "YOUR_USERNAME_HERE",
    "github_access_token": "YOUR_GITHUB_ACCESS_TOKEN_HERE",
    "branch_search_pattern": "BRANCH_NAME_REGEX_PATTERN_HERE",
    "max_repos_to_download": 300
}
```
### username
Your GitHub username
### github_access_token
The access token from GitHub with access to repositories
### branch_search_pattern
The search pattern for repositories containing a branch name matching the 
pattern
### max_repos_to_download
The maximum number of repositories to fetch information for (this can prevent 
exceeding the rate limit too quickly)

## Usage
### Download repository and branch data
```
python main.py
```

### Search for branches matching a regex pattern
```
python find_branches_by_regex.py
```
