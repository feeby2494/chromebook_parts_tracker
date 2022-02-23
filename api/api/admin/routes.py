import os
import json
from api import app, db, bcrypt
<<<<<<< HEAD
from flask import redirect, Response, request, flash, url_for
=======
>>>>>>> 961c8817091850cbe76727e8662eb657ce861414
from .models import Users

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/login")
def login():
    return Response(json.dumps({"message": "login"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/logout")
def logout():
    return Response(json.dumps({"message": "login"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/register")
def register():
<<<<<<< HEAD
    return Response(json.dumps({"message": "login"}), mimetype='application/json')
=======
    pass
>>>>>>> 961c8817091850cbe76727e8662eb657ce861414
