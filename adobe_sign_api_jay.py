import requests
import json

LOCAL_DEBUG = False                      # Print local debug info or not
API_BASE_URL = 'api/rest/v6/'

class AdobeSignAPIJay(object):

    # Creates an instance of the AdobeSign class.
    # - client_id:     See Adobe Sign > API > API Applications > YOURAPP > Configure OAuth for Application
    # - client_secret: See Adobe Sign > API > API Applications > YOURAPP > Configure OAuth for Application
    def __init__(self, client_id='', client_secret='', oauth_redirect_url=''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_redirect_url = oauth_redirect_url
        self.api_access_point = None
        self.base_uri = None
        self.token = None
        pass


    def make_oauth_url(self, scope, state=''):
        # Start with the Adobe Sign OAuth URL
        oauth_url = 'https://secure.na2.echosign.com/public/oauth?response_type=code'
        # Add the Client ID
        oauth_url += '&client_id=' + self.client_id
        # Add the Oauth redirect url
        oauth_url += '&redirect_uri=' + self.oauth_redirect_url#requests.utils.quote(self.oauth_redirect_url)
        # Add the scope
        oauth_url += '&scope=' + scope
        # Add developer-supplied state string
        oauth_url += '&state=' + state
        return (oauth_url)

    # Uses the client ID, client secret and authorization code to return a temporary access token.
    # - authorization code: The value of the 'code' parameter in the OAuth callback URL
    # - redirect_uri:  Must exactly match one of the Redirect URIs configured in
    #                  Adobe Sign > API > API Applications > YOURAPP > Configure OAuth for Application
    # Returns the access_token if the parameters are valid.
    # Returns '' otherwise.
    def get_access_token(self, authorization_code, api_access_point):
        self.authorization_code = authorization_code
        self.api_access_point = api_access_point
        
        access_token = ''
        refresh_token= ''
        if self.authorization_code and self.api_access_point:
            # Use api_access_point with the authorization code to retrieve tokens
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            payload = {
                'code': self.authorization_code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.oauth_redirect_url,
                'grant_type': 'authorization_code',
            }

            # Call the Adobe Sign API
            url = self.api_access_point + 'oauth/token'
            response = requests.post(url, headers=headers, data=payload, allow_redirects=False)

            # Process the response
            if response.status_code in (200, 201):
                data = response.json()
                print(data)
                access_token = data.get('access_token')
                refresh_token = data.get('refresh_token')
            else:
                print('AdobeSign.get_access_token() failed.')
                print('response_body:', response.text)
        return access_token, refresh_token