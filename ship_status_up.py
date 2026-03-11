import requests
import json

ClientID = ""
SecretKey = ""

OAuthURL = "https://apis-sandbox.fedex.com/oauth/token"

# Structure OAuth Request
AuthHeader = {
    'Content-Type': "application/x-www-form-urlencoded"
}

AuthReq = { 
    "grant_type": "client_credentials",
    "client_id": ClientID, 
    "client_secret": SecretKey
}

# Request and separate access token for later use
AuthResponse = requests.post(OAuthURL, data=AuthReq, headers=AuthHeader)
AccessToken = json.loads(AuthResponse.text)["access_token"]


# Fetch tracking numbers here
TrackingNum = ""

TrackURL = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

# Should probably process a request for each tracking number unless they can be done in bulk
TrackHeader = {
    "content-type": "application/json",
    "authorization": "Bearer " + AccessToken
}

TrackReq = {
    "includeDetailedScans": True,
    "trackingInfo": 
    [
        {
            "trackingNumberInfo": 
            {
                "trackingNumber": TrackingNum
            }
        }
    ]
}

# Request and process tracking information
TrackingResponse = requests.post(TrackURL, data=json.dumps(TrackReq), headers=TrackHeader)

print(TrackingResponse.text)
