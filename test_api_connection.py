import requests
import json
import base64
import sys

def get_node_details(token, node_id):
    url = "https://be.moxingshu.com/api/v1/node/detail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"id": node_id}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    # This is just a helper for the user if needed later, 
    # but my immediate task is to read the URL and compare skills.
    pass
