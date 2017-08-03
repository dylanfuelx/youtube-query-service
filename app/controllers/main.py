import os
import csv
import re
from flask import jsonify, make_response, request, redirect, url_for, session
from app import app
from app.services.youtube_query import youtube_search
from app.services.google_sheets import google_sheet_insertion
from app.utils.main import allowed_file_ext, structure_data
from app.utils.allowed_files import allowed_file_ext
from apiclient import discovery
from oauth2client import client

@app.route('/search/channel-summary', methods=['GET','POST'])
def queryAPI():
	responseObj = {}
	responseObj['status'] = True
	responseObj['data'] = []
	if request.method == 'POST':
		if not check_mimetype(request):
			return make_response(jsonify({'status':'error', 'message':'Incorrect filetype, application only accepts text/csv filetypes'}))
		if 'file' in request.files and request.files['file'].filename != '' and request.form['sheetID']:
			g_sheet_id = request.form['sheetID']
			session['sheetID'] = g_sheet_id
			file = request.files['file']
			if allowed_file_ext(file.filename,'csv'):
				file.save('../youtube-query-service/upload/tmp_file.csv')
				if 'credentials' not in session:
					return redirect(url_for('oauth2callback'))
				credentials = client.OAuth2Credentials.from_json(session['credentials'])
				if credentials.access_token_expired:
					return redirect(url_for('oauth2callback'))
				else:
					with open(os.getcwd() + '/upload' + '/tmp_file.csv','rb') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							if row[0] == 'Company':
								continue
							queryStr = row[0]
							responseObj['data'].append(youtube_search(queryStr))
					sheetValues = structure_data(responseObj['data'])
					google_sheet_insertion(sheetValues,session['sheetID'],credentials)
				return make_response(jsonify(sheetValues), 200)
			else:
				return make_response(jsonify({'status':'error','message':'incorrect file type uploaded'}), 400)
		else:
			return make_response(jsonify({'status':'error','message':'no file uploaded'}),400)
	elif request.method == 'GET':
		if 'credentials' not in session:
			return redirect(url_for('oauth2callback'))
		credentials = client.OAuth2Credentials.from_json(session['credentials'])
		if credentials.access_token_expired:
			return redirect(url_for('oauth2callback'))
		else:
			with open(os.getcwd() + '/upload' + '/tmp_file.csv','rb') as csvfile:
				reader = csv.reader(csvfile)
				for row in reader:
					if row[0] == 'Queries':
						continue
					queryStr = row[0]
					responseObj['data'].append(youtube_search(queryStr))
			sheetValues = structure_data(responseObj['data'])
			google_sheet_insertion(sheetValues,session['sheetID'],credentials)
			return make_response(jsonify(responseObj), 200)

@app.route('/auth')
def oauth2callback():
	flow = client.flow_from_clientsecrets(os.getcwd() + '/client_secret.json',scope='https://www.googleapis.com/auth/spreadsheets',redirect_uri=url_for('oauth2callback',_external=True))
	flow.params['include_granted_scopes'] = 'true'
	if 'code' not in request.args:
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		session['credentials'] = credentials.to_json()
		return redirect(url_for('queryAPI'))

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(Exception)
def unhandledException(e):
	return make_response(jsonify({'status': False, 'error': str(e)}), 500)

def check_mimetype(request):
	return 'multipart/form-data' in request.headers['Content-Type']

