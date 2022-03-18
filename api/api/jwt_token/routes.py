import json
import os
from flask import Response
from api import app
from .__token_required__ import token_required

################################################################################################################
#
#                                                  CHECK TOKEN
#
################################################################################################################

@app.route(f"/{os.environ.get('API_ROOT_URL')}/checktoken", methods=['GET'])
@token_required
def checktoken(currentUser):

    return Response(json.dumps(currentUser), mimetype='application/json'), 200


