import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

# Load variables from the .env file
load_dotenv()

# Twitter App credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')

# Define dummy values used in your .env.example
DUMMY_VALUES = ['your_api_key_here', 'your_api_secret_here', 'insert_here', '']

def is_valid(value):
    return value and value not in DUMMY_VALUES

if not is_valid(API_KEY) or not is_valid(API_SECRET):
    print("\n[!] Twitter Integration Disabled")
    print("To use this script, please replace the placeholder keys in your .env file")
    print("with real credentials from the Twitter Developer Portal.")
    exit(0) # Exit cleanly rather than crashing with an error

# Step 1: Request token
oauth = OAuth1Session(API_KEY, API_SECRET, callback_uri='http://127.0.0.1:8000/twitter/callback/')
request_token_url = 'https://api.twitter.com/oauth/request_token'

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # Step 2: Authorize app
    authorization_url = oauth.authorization_url('https://api.twitter.com/oauth/authorize')
    print("\nAuthorize your app by visiting the URL below:")
    print(authorization_url)

    # Step 3: Enter verifier
    verifier = input("\nPaste the verifier (oauth_verifier) from the redirected URL:\nVerifier: ")

    # Step 4: Request access token
    oauth = OAuth1Session(
        API_KEY,
        API_SECRET,
        resource_owner_key,
        resource_owner_secret,
        verifier=verifier
    )

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    tokens = oauth.fetch_access_token(access_token_url)

    print("\nSuccess! Add these to your .env file:")
    print(f"TWITTER_ACCESS_TOKEN={tokens['oauth_token']}")
    print(f"TWITTER_ACCESS_TOKEN_SECRET={tokens['oauth_token_secret']}")

except Exception as e:
    print(f"\n[!] An error occurred during authentication: {e}")
    print("Check if your API keys are active and your callback URL is correct.")