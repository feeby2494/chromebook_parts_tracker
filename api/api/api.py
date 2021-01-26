from api import app
import os
import json
from flask import redirect, Response

from api.data import sqlite_queries
# from flask_sqlalchemy import SQLAlchemy
#
#
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLITE_DB')
# db = SQLAlchemy(app)
# db.reflect()
#
# class Brands(db.Model):
#     __table__ = db.Model.metadata.tables['brands']
#
#     def __repr__(self):
#         return '<title %r>' % self.title
#
# def get_brands():
#     print(Brands.query.all())

# model_query.get_brands()
#Importing app from the api package! Different from my ussual methods.

@app.route('/api/chromebook_parts')
def get_chromebook_parts():
    with open(os.path.join( app.static_folder, 'json/', 'chromebook_parts.json'), 'r') as json_file:
        data = json.load(json_file)
    json_file.close()
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/api/get_brands')
def get_brands():
    data = sqlite_queries.get_brands(None)
    return Response(json.dumps(data), mimetype='application/json')
#
@app.route('/api/rebuild_json')
def rebuild_json():
    if 'chromebook_parts_dynamic.json' in os.listdir(os.path.join( app.static_folder, 'json/')):
        print("{} exists".format('chromebook_parts_dynamic.json'))
        # Forgot what I wanted to do here
    else:
        print("{} deosn't exists".format('chromebook_parts_dynamic.json'))
    #with open(os.path.join( app.static_folder, 'json/', 'chromebook_parts_dynamic.json'), 'r+') as json_file:
    #    for line in json_file:
    #        print(line)

    data = {"name": "Hi"}
    return Response(json.dumps(data), mimetype='application/json')
# @app.route('/api/get_models_for_brand/<brand_id>')
# def get_models_for_brand(brand_id):
#     data = {"name": "Hi"}
#     return Response(json.dumps(data), mimetype='application/json')

# @app.route('/api/get_brands')
# def get_brands():
#     data = {"name": "Hi"}
#     return Response(json.dumps(data), mimetype='application/json')
