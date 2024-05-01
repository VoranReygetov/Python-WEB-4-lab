import json
import pandas as pd
from datetime import datetime

json_file = 'data.json'
with open(json_file, 'r') as f:
    data = json.load(f)  # Load the existing JSON data

email = 'Manager1'
password = 'hjghjghjgh'
users_collection = data['users']
for user in users_collection:
    if user['emailUser'] == email:
        searched_user = user

# Create dictionaries for fast lookup by id
rent_data = None
for index1, rent in enumerate(data['histories']):
    if rent['user_id'] == searched_user['id'] and rent['isReturned'] == False:
        data['histories'][index1]['isReturned'] = True
        data['histories'][index1]['dateReturn'] = datetime.now
        for index2, book in enumerate(data['books']):
            if book['id'] == rent['book_id']:
                data['books'][index2]['availableBook'] =+ 1
                break
        rent_data = data['histories'][index1]
        break
    else:
            rent_data = {
            "user_id": user['id'],
            "books_id": '5b99c7eb-2db2-4e3b-bef2-2545f3b8a06e',
            "dateLoan": datetime.now,
            "isReturned": False
            }
            data['histories'].append(rent_data)
            for index, book in enumerate(data['books']):
                if book['id'] == rent['book_id']:
                    data['books'][index]['availableBook'] =- 1
                    break
with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)  # Save the updated JSON data
print(rent_data)

