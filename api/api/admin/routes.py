import os
import json
from api import app, db, bcrypt
from flask import redirect, Response, request, flash, url_for
from .models import Users

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/login")
def login():
    return Response(json.dumps({"message": "login"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/logout")
def logout():
    return Response(json.dumps({"message": "login"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/register")
def register():
    return Response(json.dumps({"message": "login"}), mimetype='application/json')