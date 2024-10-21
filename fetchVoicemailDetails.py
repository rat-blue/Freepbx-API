import requests

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
        print(f"error getting token: {response.status_code} - {response.text}")
        raise Exception("failed to get access token")

def fetch_voicemail_details(extension_id):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    query = '''
    query {
      fetchVoiceMail(extensionId: "%s") {
        status
        message
        name
        password
        context
        email
        pager
        saycid
        envelope
        attach
        delete
      }
    }
    ''' % extension_id
    
    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={'query': query}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching voicemail details: {response.status_code} - {response.text}")
        raise Exception("failed to fetch voicemail details")

if __name__ == "__main__":
    try:
        voicemail_details = fetch_voicemail_details(EXTENSION_ID)
        print(voicemail_details)
    except Exception as e:
        print(f"error occurred: {e}")
