from flask import jsonify, make_response
from app import app
from app.services.youtube_query import youtube_search

@app.route('/make-query', methods=['GET'])
def queryAPI():
	
	return make_response(jsonify(youtube_search()), 200)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(Exception)
def unhandledException(e):
	return make_response(jsonify({'error': str(e)}), 500)