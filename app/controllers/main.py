import csv
import re
from flask import jsonify, make_response, request
from app import app
from app.services.youtube_query import youtube_search
from app.services.google_sheets import google_sheet_insertion
<<<<<<< HEAD
from app.utils.main import allowed_file_ext, format_data_array
=======
from app.utils.main import allowed_file_ext, structure_data
>>>>>>> jason/utils

@app.route('/search/channel-summary', methods=['POST'])
def queryAPI():
	if not check_mimetype(request):
		return make_response(jsonify({'status':'error', 'message':'Incorrect filetype, application only accepts text/csv filetypes'}))
	if 'file' in request.files and request.files['file'].filename != '' and request.form['sheetID']:
		file = request.files['file']
		g_sheet_id = request.form['sheetID']
		if allowed_file_ext(file.filename,'csv'):
			responseObj = {}
			responseObj['status'] = True
			responseObj['data'] = []

			reader = csv.reader(file)
			for row in reader:
				if row[0] == 'Queries':
					continue
				queryStr = row[0]
				responseObj['data'].append(youtube_search(queryStr))

			sheetValues = structure_data(responseObj['data'])
			google_sheet_insertion(sheetValues, g_sheet_id)
			return make_response(jsonify(sheetValues), 200)
		else:
			return make_response(jsonify({'status':'error','message':'incorrect file type uploaded'}), 400)
	else:
		return make_response(jsonify({'status':'error','message':'no file uploaded'}),400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(Exception)
def unhandledException(e):
	return make_response(jsonify({'status': False, 'error': str(e)}), 500)

def check_mimetype(request):
	return 'multipart/form-data' in request.headers['Content-Type']
