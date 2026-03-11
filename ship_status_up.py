import requests
import json
import os
import time
import datetime

CLIENTID = os.environ.get('FED_PUB_KEY')
SECRETKEY = os.environ.get('FED_SEC_KEY')

OAUTHURL = "https://apis-sandbox.fedex.com/oauth/token"
TRACKURL = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

# NOTE: Find a way to gracefully exit on restart, sigterm, sigint, sigkill

# TODO: Error checking
def fetchAuthToken():

    if CLIENTID == None or SECRETKEY == None:
        print("API Credentials Not Found")
        exit()

    # Structure OAuth Request
    authHeader = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    authReq = { 
        "grant_type": "client_credentials",
        "client_id": CLIENTID, 
        "client_secret": SECRETKEY
    }

    # Request and separate access token for later use
    authResponse = requests.post(OAUTHURL, data=authReq, headers=authHeader)
    accessToken = json.loads(authResponse.text)["access_token"]
    
    return accessToken

# TODO: Error checking
def fetchTrackingStatus(TrackingNum, accessToken):

    # Fetch tracking numbers here
    # TrackingNum = "499496853570"

    # Should probably process a request for each tracking number unless they can be done in bulk
    trackHeader = {
        "content-type": "application/json",
        "authorization": "Bearer " + accessToken
    }

    trackReq = {
        "includeDetailedScans": True,
        "trackingInfo": 
        [
            {
                "trackingNumberInfo": 
                {
                    "trackingNumber": trackingNum
                }
            }
        ]
    }

    # Request and process tracking information
    trackingResponse = requests.post(TRACKURL, data=json.dumps(trackReq), headers=trackHeader)

    return trackingResponse

# Define remaining access time and desired update rate
accessTokenRemainingTime = 0
accessToken = None
updateRate = 60

# Loop until break
while True:

    if accessTokenRemainingTime <= updateRate:
        accessToken = fetchAuthToken()
        accessTokenRemainingTime = 3600
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Renewed OAuth Token")

    # Should grab relevant records here and store in array/dict keying off tracking numbers
    print(f"Current remaining auth time is {accessTokenRemainingTime} seconds")
    # Iterate over items in aforementioned record dict, updating database records as we go

    time.sleep(updateRate)
    accessTokenRemainingTime = accessTokenRemainingTime - updateRate

