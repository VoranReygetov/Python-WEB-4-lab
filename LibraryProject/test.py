import json
import pandas as pd
from datetime import datetime

json_file = 'data.json'
with open(json_file, 'r') as f:
    data = json.load(f)  # Load the existing JSON data

email = "Manager1@ffdsfk.com"
password = 'hjghjghjgh'
searched_user = None
users_collection = data['users']
for user in users_collection:
    if user['emailUser'] == email and user['is_admin'] == False:
        print(user)

# print(data['users'])

