import logging
import os
import sys
from flask import Flask, redirect, Response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy  import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


load_dotenv()


# try:
#     SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DB')
# except NameError:
#     print("cannot access db")

# from models.chromebook_inventory import db, brands, models, repairs, parts, locations, inventories

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB')

db = SQLAlchemy(app)

# init Migrate
migrate = Migrate(app, db, render_as_batch=True)

# for user passwords
bcrypt = Bcrypt(app)

# Importing DB models
# import models.chromebook_inventory
print(sys.path)


# Importing API and View modules
import api.api
import api.admin.routes
import api.token.routes

if __name__ == '__main__':
    app.run(debug=True)
