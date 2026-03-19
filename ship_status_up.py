import requests
import json
import os
import time
import datetime
import pyodbc
import nacl.secret
import nacl.utils
from sqlalchemy import create_engine, text, event
from sqlalchemy.engine import URL

CLIENT = os.environ.get('FED_PUB_KEY')
SECRET = os.environ.get('FED_SEC_KEY')

OAUTHURL = "https://apis-sandbox.fedex.com/oauth/token"
TRACKURL = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

# NOTE: Find a way to gracefully exit on restart, sigterm, sigint, sigkill

"""
Returns String OAuth access token
"""
def fetchAuthToken(clientID, secretKey):

    if clientID == None or secretKey == None:
        print("API Credentials Not Found")
        exit()

    # Structure OAuth Request
    authHeader = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    authReq = { 
        "grant_type": "client_credentials",
        "client_id": clientID, 
        "client_secret": secretKey
    }

    # Request and separate access token for later use
    try:
        authResponse = requests.post(OAUTHURL, data=authReq, headers=authHeader)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    accessToken = json.loads(authResponse.text)["access_token"]
    
    return accessToken

"""
Returns JSON tracking status when provided with a tracking number and access token in the form of strings
"""
def fetchTrackingStatus(TrackingNum, accessToken):

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
    try:
        trackingResponse = requests.post(TRACKURL, data=json.dumps(trackReq), headers=trackHeader)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return trackingResponse

# NOTE: Will require testing in remote environment
"""
Returns SQL engine object when provided with MJL DB credentials in the form of a string
"""
def connectMJLDatabase():

    creds = None
    # NOTE: Will have to find a more permanent residence for the encrypted credentials if we want to continue using this
    # solution
    with open("", "br") as key_f:
        with open("", "br") as df_f:
            box = nacl.secret.SecretBox(key_f.read())
            creds = box.decrypt(df_f.read()).decode('utf-8')

    if creds != None:
        connection_string = f"Driver={{SQL Server Native Client 11.0}};Server=localhost;UID=sa;PWD={creds};Database=MJLTest"
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url, fast_executemany=True)
        return engine
    else:
        print("Error parsing credentials")

"""
Returns list of tracking numbers from provided database engine
"""
def fetchOpenOrderTrackingNumbers(engine):
    # Query

    # Parsing returned records

    # trackingNumbers = list of tuples or dict
    
    return trackingNumbers

# ENTRY POINT #

if __name__ == "__main__":

    accessTokenRemainingTime = 0
    accessToken = None
    updateRate = 60

    while True:

        if accessTokenRemainingTime <= updateRate:
            accessToken = fetchAuthToken(CLIENT, SECRET)
            accessTokenRemainingTime = 3600
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Renewed OAuth Token")

        # Should grab relevant records here and store in array/dict keying off tracking numbers
        print(f"Current remaining auth time is {accessTokenRemainingTime} seconds")
        # Iterate over items in aforementioned record dict, updating database records as we go

        time.sleep(updateRate)
        accessTokenRemainingTime = accessTokenRemainingTime - updateRate

