# Description: This script fetches the information of all the datasets available on the Fingrid Open Data API.
# mika.saari@tuni.fi
# Last updated: 2021-10-06

import os
import urllib.request, json
import ssl
import time
# add your API key to system environment variables
# export API_KEY='your_api_key'

api_key = os.getenv('API_KEY')
# or you can directly assign the API key here

# List to store dataset IDs with "Error 404"
error_404_ids = []

# Initial dataset ID to start fetching information (75 is only for example)
dataset_id = '75'

# List to store dataset information
datasets_info = []

for dataset_id in range(1, 251):
    try:
        url = f"https://data.fingrid.fi/api/datasets/{dataset_id}"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'x-api-key': api_key,
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: 'GET'
        context = ssl._create_unverified_context()

        response = urllib.request.urlopen(req, context=context)
        
        #print(response.getcode())
        #print(response.read())

        # Parse the JSON response
        data = json.loads(response.read().decode('utf-8'))
        
        # Extract and print the required fields
        dataset_id = data.get('id')
        name = data.get('nameEn')  # Assuming you want the English name
        
        #print(f"id: {dataset_id}")
        #print(f"name: {name}")

        datasets_info.append({'id': dataset_id, 'name': name})


    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_404_ids.append(dataset_id)
    except Exception as e:
        #print(e)
        print(f"Error fetching dataset {dataset_id}: {e}")
    time.sleep(2)  # Sleep for 1 second to avoid hitting the rate limit

# Print the list of dataset information
print("Dataset Information:")
print(datasets_info)

# Print the list of dataset IDs with "Error 404"
print("Dataset IDs with Error 404:")
print(error_404_ids)

with open('datasets_info.txt', 'w') as file:
    json.dump(datasets_info, file, indent=4)
####################################