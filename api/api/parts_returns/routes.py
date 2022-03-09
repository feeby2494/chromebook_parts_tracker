import os
import json
from api import app, db
from flask import Response, request, url_for
from api.token.__token_required__ import token_required
from .generate_csv_for_cyma import generate_csv_for_cyma
from .generate_csv_for_mobilesentrix import generate_csv_for_mobilesentrix

@app.route(f"/{os.environ.get('API_ROOT_URL')}/return_parts_for_mobsen", methods=['GET'])
def return_parts_for_mobsen():
    return ''


@app.route(f"/{os.environ.get('API_ROOT_URL')}/return_parts_for_mobsen", methods=['GET'])
def return_parts_for_mobsen():
    return ''