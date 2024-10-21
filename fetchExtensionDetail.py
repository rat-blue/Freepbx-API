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

def fetch_extension(access_token, extension_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    query = """
    query {
        fetchExtension(extensionId: "%s") {
            status
            message
            id
            extensionId
            user {
                name
                outboundCid
                voicemail
                ringtimer
                noanswer
                noanswerDestination
                noanswerCid
                busyCid
                sipname
                password
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
    """ % (extension_id)

    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={'query': query}
    )

    print("fetching extension:", response.status_code, response.text)

    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('fetchExtension', {})
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        token = get_access_token()
        extension_details = fetch_extension(token, extension_id)

        if extension_details and extension_details.get('status'):
            print("extension details:")
            print(json.dumps(extension_details, indent=4))
        else:
            print("failed to fetch extension")
    except Exception as e:
        print("error:", str(e))
