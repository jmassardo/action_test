import os
import requests
import json

print("Attempting to parse the pull request env var.")
# Read the environment variable
pull = os.getenv('PULL_PAYLOAD')

# Personal access token from your GitHub account
token = os.getenv('GITHUB_TOKEN')

# The repository to add this issue to
repo_owner = pull["base"]["repo"]["owner"]["login"]
repo_name = pull["base"]["repo"]["name"]

print(repo_owner)
print(repo_name)

# Parse the checklist items from the PR body
def parse_checklist():
    # Split the string into lines
    lines = pr["body"].split('\\r\\n')
    print(lines)

    # Parse the checklist items
    checklist_items = [line.replace('- [ ]', '').strip()
                       for line in lines if line.startswith('- [ ]')]
    tasks = [item.replace('COMPLIANCE-', '') for item in checklist_items]
    return tasks

print(parse_checklist())