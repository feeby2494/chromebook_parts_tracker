from api import app
import os
import json
from flask import redirect, Response
from api.data import select_queries
from api.models.chromebook_inventory import db, Brands, Models, Repairs, Parts, Inventories, Locations

#Importing app from the api package! Different from my ussual methods.

@app.route('/api/chromebook_parts')
def get_chromebook_parts():
    with open(os.path.join( app.static_folder, 'json/', 'chromebook_parts.json'), 'r') as json_file:
        data = json.load(json_file)
    json_file.close()
    return Response(json.dumps(data), mimetype='application/json')

# @app.route('/api/get_brands')
# def get_brands():
#     data = {"name": "Hi"}
#     return Response(json.dumps(data), mimetype='application/json')
#
@app.route('/api/rebuild_json')
def rebuild_json():
    if 'chromebook_parts.json' in os.listdir(os.path.join( app.static_folder, 'json/')):
        print("{} exists".format('chromebook_parts.json'))
    else:
        print("{} deosn't exists".format('chromebook_parts.json'))
    #with open(os.path.join( app.static_folder, 'json/', 'chromebook_parts_dynamic.json'), 'r+') as json_file:
    #    for line in json_file:
    #        print(line)

    data = {"name": "Hi"}
    return Response(json.dumps(data), mimetype='application/json')
# @app.route('/api/get_models_for_brand/<brand_id>')
# def get_models_for_brand(brand_id):
#     data = {"name": "Hi"}
#     return Response(json.dumps(data), mimetype='application/json')

@app.route('/api/get_brands')
def get_brands():
    brands = []
    data = db.session.query(Brands).all()
    for brand in data:
        brands.append(brand.brand_name)
    return Response(json.dumps({"brands": brands}), mimetype='application/json')

@app.route('/api/get_models/<brand_name>')
def get_models(brand_name):
    brand_id = db.session.query(Brands).filter_by(brand_name=brand_name).first().brand_id
    print(brand_id)
    models = []
    data = db.session.query(Models).filter_by(brand_id=brand_id).all()
    for model in data:
        models.append(model.model_name)
    return Response(json.dumps({"models": models}), mimetype='application/json')

@app.route('/api/get_repairs/<model_name>')
def get_repairs(model_name):
    model_id = db.session.query(Models).filter_by(model_name=model_name).first().model_id
    print(model_id)
    repairs = {}
    data = db.session.query(Repairs).filter_by(model_id=model_id).all()
    for repair in data:
        repairs[repair.repair_type] = {}
        repairs[repair.repair_type]["repair_type"] = repair.repair_type
        repairs[repair.repair_type]["repair_area"] = repair.repair_area
        repairs[repair.repair_type]["model_id"] = repair.model_id
    return Response(json.dumps(repairs), mimetype='application/json')

@app.route('/api/get_parts/<repair_type>')
def get_parts(repair_type):
    repair_id = db.session.query(Repairs).filter_by(repair_type=repair_type).first().repair_id
    print(repair_id)
    parts = {}
    parts_data = db.session.query(Parts).filter_by(repair_id=repair_id).all()
    print(parts_data)
    for part in parts_data:
        print(part.part_number)
        parts[part.part_number] = {}
        parts[part.part_number]['part_number'] = part.part_number
        parts[part.part_number]["model_id"] = part.model_id
        parts[part.part_number]["repair_id"] = part.repair_id
    # inventory_data
    return Response(json.dumps(parts), mimetype='application/json')
