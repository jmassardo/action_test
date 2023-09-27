import os
import requests
import json

print("Attempting to parse the pull request env var.")
# Read the environment variable
pull = os.getenv('PULL_PAYLOAD')

print(pull)