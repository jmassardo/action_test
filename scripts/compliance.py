import os
import requests
import json

# Read the environment variable
pull = json.loads(os.getenv('PULL_PAYLOAD'))

print(pull)
# Personal access token from your GitHub account
token = os.getenv('GITHUB_TOKEN')

# The repository to add this issue to
repo_owner, repo_name = pull["base"]["repo"]["full_name"].split('/')

# Parse the checklist items from the PR body
def parse_checklist():
    # Split the string into lines
    lines = pull["body"].split('\r\n')
    print(lines)

    # Parse the checklist items
    checklist_items = [line.replace('- [ ]', '').strip()
                       for line in lines if line.startswith('- [ ]')]
    tasks = [item.replace('COMPLIANCE-', '') for item in checklist_items]
    print(tasks)
    return tasks

# Create a new GitHub issue
def create_github_issue(task ):
    # Create a GitHub issue
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Issue data
    data = {
        "title": "COMPLIANCE-" + task + "-" + str(pull["number"]),
        "body": "This issue was automatically created from a tasklist item in the PR body.",
        "labels": ["compliance"],
        "assignees": [pull["user"]["login"]]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check for errors
    response.raise_for_status()

    # Return the issue number
    return response.json().get('number')

# Parse the checklist items from the PR body
checklist = parse_checklist()

# Make an array so we can track the new issues we make
issue_numbers = []

# Loop through the tasks we parsed earlier and make issues for each one.
for task in checklist:
    print(f"Creating issue for task {task}")
    issue_number = create_github_issue(task)
    issue_numbers.append(issue_number)
    print(f"Created issue #{issue_number} for task {task}")

# Now we have a list of issue numbers, let's replace the existing tasklist with a new one containing links to the issues we just created.
original_pr_body = pull["body"]

# Create a new tasklist
new_tasklist = []
for issue_number in issue_numbers:
    new_tasklist.append(f"- [ ] #{issue_number}")

# Replace the old tasklist with the new one
new_pr_body = original_pr_body.split('\r\n')
new_pr_body = [line for line in new_pr_body if not line.startswith('- [ ]')]
# Remove the last line so the checklist doesn't get dorked up
new_pr_body.pop()
new_pr_body = new_pr_body + new_tasklist
new_pr_body = '\r\n'.join(new_pr_body)
new_pr_body = new_pr_body + '\r\n```'
# Update the PR with the new tasklist
pr_url = pull["url"]

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# The new data for the pull request
data = {
    "title": pull["title"],
    "body": new_pr_body,
    "state": "open"
}
print(data)
response = requests.patch(pr_url, headers=headers, data=json.dumps(data))
print(response)
# Check for errors
response.raise_for_status()