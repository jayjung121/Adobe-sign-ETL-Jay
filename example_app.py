from flask import Flask, request, current_app, render_template, redirect, url_for
from adobe_sign_api_jay import AdobeSignAPIJay

# Create a web application with Flask
app = Flask(__name__)

# Copy local_settings.py from local_settings_example.py
## Edit local_settings.py to reflect your CLIENT_ID and CLIENT_SECRET
app.config.from_pyfile('local_settings.py')    # Read example_app.local_settings.py

# Initialize the AdobeSign package
adobesign_api = AdobeSignAPIJay(
        app.config.get('ADOBE_SIGN_CLIENT_ID'),
        app.config.get('ADOBE_SIGN_CLIENT_SECRET'),
        app.config.get('ADOBE_SIGN_REDIRECT_URL'))


# Display the home page
@app.route('/')
def home_page():
    # This link will cause Adobe Sign to redirect to
    # 'https://localhost:5443/adobe_sign/oauth_redirect' with authentication information
    oauth_url = adobesign_api.make_oauth_url(
            'user_login:account+agreement_read:account', # authorization scope
            '')                                                                 # developer-supplied state string
        
    # token will be None on the first visit, and will hold the access token on subsequent visits
    access_token = request.args.get('token')
    refresh_token = request.args.get('refreshtoken')
    #adobesign_api.token = access_token

    print("acc", access_token)
    # Render the home page
    return render_template('layout.html',
            oauth_url=oauth_url,
            access_token=access_token,
            refresh_token=refresh_token
            )



# Adobe Sign will redirect to this URL (https://localhost:5443/adobe_sign/oauth_redirect)
# in response to an authorization request (https://secure.na1.echosign.com/public/oauth).
@app.route('/adobe_sign/oauth_redirect')
def oauth_redirect():

    # Authentication info is passed in the GET query parameters
    # - code:              Authentication code
    # - api_access_point:  Points to the proper api server (https://secure.na1.echosign.com/)
    # - state:             Developer-supplied state string
    authorization_code = request.args.get('code')  
    api_access_point = request.args.get('api_access_point')
    state = request.args.get('state')
    print(authorization_code)
    print(api_access_point)  
    # Use authorization_code and api_access_point to retrieve an access token
    access_token, refresh_token = adobesign_api.get_access_token(authorization_code, api_access_point)
    #assert(access_token)

    # Redirect back to the home page, but this time with the access token
    return redirect(url_for('home_page')+'?token='+access_token+'&refreshtoken='+refresh_token)

