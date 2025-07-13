from requests_oauthlib import OAuth1Session

# Twitter App credentials
API_KEY = 'sxaXZ2OVzJl38h4o28oDZo06D'
API_SECRET = 'nrkJR1l2udVWgAa8ZrgRy0ik6lpY5Egv76FWAxcXdCXDcX5ia3'

# Step 1: Request token
oauth = OAuth1Session(API_KEY, API_SECRET, callback_uri='http://127.0.0.1:8000/twitter/callback/')
request_token_url = 'https://api.twitter.com/oauth/request_token'
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

print("\nAccess Token:", tokens['oauth_token'])
print("Access Token Secret:", tokens['oauth_token_secret'])
