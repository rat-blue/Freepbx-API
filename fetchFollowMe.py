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
        print(f"error getting token: {response.status_code} - {response.text}")
        raise Exception("failed to get access token")

def fetch_follow_me(access_token, extension_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    query = """
    query {
        fetchFollowMe(extensionId: "%s") {
            id
            message
            status
            enabled
            extensionId
            strategy
            ringTime
            followMePrefix
            followMeList
            callerMessage
            noAnswerDestination
            alertInfo
            confirmCalls
            receiverMessageConfirmCall
            receiverMessageTooLate
            ringingMusic
            initialRingTime
            voicemail
            enableCalendar
            calendar
            calendarGroup
            matchCalendar
            overrideRingerVolume
            externalCallerIdMode
            fixedCallerId
        }
    }
    """ % (extension_id)

    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={'query': query}
    )

    print("fetching follow me:", response.status_code, response.text)

    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('fetchFollowMe', {})
    else:
        print(f"error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        token = get_access_token()
        follow_me_details = fetch_follow_me(token, extension_id)

        if follow_me_details and follow_me_details.get('status'):
            print("follow Me details:")
            print(json.dumps(follow_me_details, indent=4))
        else:
            print("failed to fetch Follow Me details")
    except Exception as e:
        print("error:", str(e))
