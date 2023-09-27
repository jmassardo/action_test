import os
import requests
import json

# Read the environment variable
payload = os.getenv('EVENT_PAYLOAD')

print(payload)