import requests
import json

TOKEN_URL = 'TOKEN URL'
GRAPHQL_URL = 'GQL URL'
CLIENT_ID = 'CLIENT ID'
CLIENT_SECRET = 'CLIENT SECRET'
EXTENSION_ID = "EXTENSION ID"

def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error getting token: {response.status_code} - {response.text}")
        raise Exception("failed to get access token")

def fetch_all_extensions(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    query = """
    query {
        fetchAllExtensions {
            status
            message
            totalCount
            extension {
                id
                extensionId
                user {
                    name
                    password
                    outboundCid
                    ringtimer
                    noanswer
                    sipname
                    extPassword
                }
                coreDevice {
                    deviceId
                    dial
                    devicetype
                    description
                    emergencyCid
                }
            }
        }
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={'query': query}
    )

    print("fetching all extensions:", response.status_code, response.text)

    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('fetchAllExtensions', {})
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        token = get_access_token()
        all_extensions = fetch_all_extensions(token)

        if all_extensions and all_extensions.get('status'):
            print("all extensions details:")
            print(json.dumps(all_extensions, indent=4))
        else:
            print("failed to fetch all extensions")
    except Exception as e:
        print("error:", str(e))
