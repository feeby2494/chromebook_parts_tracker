from functools import wraps
from flask import request, Response
from api import app
from api.user.models import Users
import jwt
import json

################################################################################################################
#
#                                                  DECORATORS
#
################################################################################################################

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        """
            Decorator to require jwt token for a specified route.
        """

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return Response(json.dumps({'message' : 'Token is missing'}), mimetype='application/json'), 401

        try:
            #pyJwt has changed since the tortoral from PrettyPrinted: algorithms=["HS256"] must be passed as an argument to jwt.decode; change "HS256" to what algorithm yiu sued to encode your jwt
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            
        except:

            return Response(json.dumps({'message' : 'Token is invalid'}), mimetype='application/json'), 401

        return f(current_user, *args, **kwargs)

    return decorated
