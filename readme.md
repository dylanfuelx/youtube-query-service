Everything you need to know about the Youtube Query Serivce

Setting up developer environment:

This is a flask app, so first things first, you will need to get your virtual environment set up and install flask. Docs are here: http://flask.pocoo.org/docs/0.12/installation/

Once you have your virtual environment set up and flask installed, two more modules need to be pip installed: Google API Client for Python and the python Oauth2Client.

$ pip install --upgrade google-api-python-client

$ pip install --upgrade oauth2client

Using the App:

For development - Run the app in debug mode via dev-run.py (python dev-run.py)

For production - The entrypoint into the app will be wsgi.py


Credentials for running locally:

Enable the YouTube and Google Sheets API's via Google's Dev console. Then download the client_secret.json and replace the version in this repo with your fancy new keys.

You will also need to replace the YouTube API key in services/youtube_query.py with an API key you make in the Google console as well.