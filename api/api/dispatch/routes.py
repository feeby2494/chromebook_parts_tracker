import os
import json
from api import app, db, bcrypt
from flask import redirect, Response, request, flash, url_for
# from .models import Users
from api.jwt_token.__token_required__ import token_required
import uuid
from sqlalchemy import exc
from flask_cors import CORS


################################################################################################################
#
#                                                  Handle Local Dropoffs - Detrack API
#
################################################################################################################


@app.route(f"/{os.environ.get('API_ROOT_URL')}/new_dispatch", methods=['GET', 'POST'])
def new_dispatch():
    """
        API route to update status of dispatch orders
    """

    if request.method == "POST":
        print(request.json)
        return Response(json.dumps(request.json), mimetype='application/json')
    
    

    return Response(json.dumps({"message": "hi"}), mimetype='application/json')


################################################################################################################
#
#                                                  Handle Status Update from Detrack Webhooks
#
################################################################################################################

@app.route(f"/{os.environ.get('API_ROOT_URL')}/update_dispatch", methods=['GET', 'POST'])
def update_dispatch():
    """
        API route to update status of dispatch orders
    """

    if request.method == "POST":
        print(request.json)
        return Response(json.dumps(request.json), mimetype='application/json')
    
    

    return Response(json.dumps({"message": "hi"}), mimetype='application/json')