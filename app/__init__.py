from flask import Flask
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app, resources={r"/search/*": {"origins":"*"}})

from app.controllers import main


