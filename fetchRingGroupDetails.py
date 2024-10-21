import requests
import json

TOKEN_URL = 'TOKEN URL'
GRAPHQL_URL = 'GQL URL'
CLIENT_ID = 'CLIENT ID'
CLIENT_SECRET = 'CLIENT SECRET'
group_number = 'RING GROUP NUMBER'

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

def fetch_ring_group(access_token, group_number):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    query = """
    query {
        fetchRingGroup(groupNumber: "%s") {
            status
            message
            groupNumber
            description
            groupTime
            groupList
            strategy
            groupPrefix
            needConf
            ignoreCallForward
            ignoreCallWait
            pickupCall
            callRecording
            callProgress
            answeredElseWhere
            overrideRingerVolume
        }
    }
    """ % (group_number)

    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={'query': query}
    )

    print("fetching ring group:", response.status_code, response.text)

    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('fetchRingGroup', {})
    else:
        print(f"error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        token = get_access_token()
        ring_group_details = fetch_ring_group(token, group_number)

        if ring_group_details and ring_group_details.get('status'):
            print("ring group:")
            print(json.dumps(ring_group_details, indent=4))
        else:
            print("failed to fetch ring group")
    except Exception as e:
        print("error:", str(e))
