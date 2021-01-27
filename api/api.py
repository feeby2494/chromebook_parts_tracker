import os
import logging
import json

from flask import Flask, redirect, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/chromebook_parts')
def get_chromebook_parts():
    json_file = open(os.path.join( app.static_folder, 'json/', 'chromebook_parts.json'), 'r')
    data = json.load(json_file)
    print(data)
    return Response(json.dumps(data), mimetype='application/json')
