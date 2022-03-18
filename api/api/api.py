from api import app
import os
import json
import csv
from flask import redirect, Response, request, flash, url_for
from werkzeug.utils import secure_filename
from api.data import select_queries
from api.models.chromebook_inventory import db, Brands, Models, Repairs, Parts, Inventories, Locations, part_repair_association
import urllib.parse
import xlrd
from api.emails import generate_then_send
from api.data import sqlite_queries
from api.jwt_token.__token_required__ import token_required



# @async
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     send_async_email(app, msg)

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

# Upload Folder Setup

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route(f"/{os.environ.get('API_ROOT_URL')}/chromebook_parts")
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
@app.route(f"/{os.environ.get('API_ROOT_URL')}/rebuild_json")
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

@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_brands", methods = ['GET', 'POST', 'DELETE'])
def get_brands():
    def get_brands_json():
        brands = []
        data = db.session.query(Brands).all()
        for brand in data:
            brands.append(brand.brand_name)
        return brands

    if request.method == 'GET':
        brands = get_brands_json()
        return Response(json.dumps({"brands": brands}), mimetype='application/json')

    if request.method == 'POST':
        data = request.get_json()
        print(data["brand_name"])
        # Make sure I get right value first, and use test db on local computer
        new_brand = Brands(brand_name=data["brand_name"])
        db.session.add(new_brand)
        db.session.commit()
        brands = get_brands_json()
        return Response(json.dumps({"brands": brands}), mimetype='application/json')

    if request.method == 'DELETE':
        # Not even going to make this possible right now!
        data = request.get_json()
        brand_to_delete = db.session.query(Brands).filter_by(brand_name=data["brand_name"]).first()
        db.session.delete(brand_to_delete)
        db.session.commit()
        brands = get_brands_json()
        return Response(json.dumps({"brands": brands}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/resolve_model_from_part_number/<path:part_number>", methods = ['GET'])
def get_model_from_part(part_number):

    # URL decode part_number first:
    part_number = urllib.parse.unquote(part_number)
    print(part_number)

    # for association in repair.parts:
    #         parts_for_repair[association.part_number] = {}
    #         parts_for_repair[association.part_number]['part_number'] = association.part_number
    #         parts_for_repair[association.part_number]["model_id"] = association.model_id
    #         parts_for_repair[association.part_number]["part_id"] = association.part_id
    #         if association.part_info:
    #             parts_for_repair[association.part_number]["part_info"] = association.part_info

    repairs_for_this_part = []

    # Need part_id to look up part_repair_association table
    part = db.session.query(Parts).filter_by(part_number = part_number).first()
    if part:
        for association in part.repair_list:
            repair_id = association.repair_id
            repair_query = db.session.query(Repairs).filter_by(repair_id = repair_id).first()
            if repair_query:
                repair_name = repair_query.repair_type
                repair_object = {}
                repair_object['name'] = repair_name
                repair_object['id'] = repair_id
                repairs_for_this_part.append(repair_object)
    
    return Response(json.dumps({"repairs": repairs_for_this_part}), mimetype='application/json')


@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_models/<brand_name>", methods = ['GET', 'POST', 'DELETE'])
def get_models(brand_name):

    # URL decode model_name first:
    brand_name = urllib.parse.unquote(brand_name)
    print(brand_name)

    def get_brand_id():
        brand_id = db.session.query(Brands).filter_by(brand_name=brand_name).first().brand_id
        return brand_id

    brand_id = get_brand_id()

    def get_models_json(brand_id):
        models = []
        data = db.session.query(Models).filter_by(brand_id=brand_id).all()
        for model in data:
            models.append(model.model_name)
        return models
    if request.method == 'GET':
        models = get_models_json(brand_id)
        return Response(json.dumps({"models": models}), mimetype='application/json')

    if request.method == 'POST':
        data = request.get_json()
        new_model = Models(model_name=data["model_name"], brand_id=brand_id)
        db.session.add(new_model)
        db.session.commit()

        models = get_models_json(brand_id)
        return Response(json.dumps({"models": models}), mimetype='application/json')

    # if request.method == 'PUT':
    #     brand_id = get_brand_id()
    #     # Don't know how PUT reqesut works
    #     data = request.form.get("model_name")
    #     model_to_mod = db.session.query(Models).filter_by(model_name=data).first()
    #     db.session.put(model_to_mod)
    # #     db.session.commit()
    #
    #     models = get_models_json(brand_id)
    #     return Response(json.dumps({"models": models}), mimetype='application/json')

    if request.method == 'DELETE':
        data = request.get_json()
        model_to_delete = db.session.query(Models).filter_by(model_name=data["model_name"]).first()
        db.session.delete(model_to_delete)
        db.session.commit()

        models = get_models_json(brand_id)
        return Response(json.dumps({"models": models}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_repairs/<model_name>", methods = ['GET', 'POST', 'DELETE'])
def get_repairs(model_name):

    # URL decode model_name first:
    model_name = urllib.parse.unquote(model_name)

    def get_model_id():
        model_id = db.session.query(Models).filter_by(model_name=model_name).first().model_id
        return model_id

    if model_name != "add_model":
        model_id = get_model_id()

    def get_repairs_json(model_id):
        repairs = {}
        data = db.session.query(Repairs).filter_by(model_id=model_id).all()
        for repair in data:
            repairs[repair.repair_type] = {}
            repairs[repair.repair_type]["repair_type"] = repair.repair_type
            repairs[repair.repair_type]["repair_area"] = repair.repair_area
            repairs[repair.repair_type]["model_id"] = repair.model_id
        return repairs

    if request.method == 'GET':
        if model_name != "add_model":
            repairs = get_repairs_json(model_id)
            return Response(json.dumps(repairs), mimetype='application/json')
        return Response(json.dumps({"message":"No repairs for this model yet"}), mimetype='application/json')

    if request.method == 'POST':
        repair_type = request.get_json()["repair_type"]
        repair_area = request.get_json()["repair_area"]
        new_repair = Repairs(repair_type=repair_type,repair_area=repair_area, model_id=model_id)
        db.session.add(new_repair)
        db.session.commit()

        repairs = get_repairs_json(model_id)
        return Response(json.dumps(repairs), mimetype='application/json')

    if request.method == 'DELETE':
        data = request.get_json()["repair_type"]
        repair_to_delete = db.session.query(Repairs).filter_by(repair_type=data).first()
        db.session.delete(repair_to_delete)
        db.session.commit()

        repairs = get_repairs_json(model_id)
        return Response(json.dumps(repairs), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_parts/<repair_type>", methods = ['GET', 'POST', 'DELETE'])
def get_parts(repair_type):

    # URL decode model_name first:
    repair_type = urllib.parse.unquote(repair_type)

    # def get_repair_id():
    #     repair_id = db.session.query(Repairs).filter_by(repair_type=repair_type).first().repair_id
    #     return repair_id
    #
    # repair_id = get_repair_id()

    def get_parts_json(repair):

        # Create our json return object full of parts for this repair:
        parts_for_repair = {}

        # for item in part_repair_association:
        #     if item.repair_id == repair.repair_id:
        #         parts_for_repair[association.part_number] = {}
        #         parts_for_repair[association.part_number]['part_number'] = association.part_number
        #         parts_for_repair[association.part_number]["model_id"] = association.model_id
        #         parts_for_repair[association.part_number]["part_id"] = association.part_id

        # I don't understand the error here, if no parts, then repair.parts should be []
        for association in repair.parts:
            parts_for_repair[association.part_number] = {}
            parts_for_repair[association.part_number]['part_number'] = association.part_number
            parts_for_repair[association.part_number]["model_id"] = association.model_id
            parts_for_repair[association.part_number]["part_id"] = association.part_id
            if association.part_info:
                parts_for_repair[association.part_number]["part_info"] = association.part_info


        return parts_for_repair

    def get_inventories(part_id):
        inventory_by_location = {}
        inventories = db.session.query(Inventories).filter_by(part_id=part_id).all()
        for inventory in inventories:
            inventory_by_location[inventory.location_id] = {}
            inventory_by_location[inventory.location_id]['count'] = inventory.count
            inventory_by_location[inventory.location_id]['part_id'] = inventory.part_id
        return inventory_by_location


    if request.method == 'GET':
        # I don't understand the error here
        # repair = db.session.query(Repairs).filter_by(repair_type=repair_type).first()
        repair = Repairs.query.filter_by(repair_type=repair_type).first()
        parts = get_parts_json(repair)
        inventory = {}
        for part in parts:
            if parts[part]["part_id"] is not None:
                inventory[part] = get_inventories(parts[part]["part_id"])
        return Response(json.dumps([parts, inventory]), mimetype='application/json')

    if request.method == 'POST':

        # Define common vars
        repair = db.session.query(Repairs).filter_by(repair_type=repair_type).first()
        model_id = repair.model_id
        part_number = request.get_json()["part_number"]
        part_info = request.get_json()["part_info"]

        # 0. Check if part already exists
        part_exists = db.session.query(Parts).filter_by(part_number=part_number).first()
        if part_exists:
            # Check if the part_info field was updated:
            if part_info:
                # if differnet and not blank, then change part_exists.part_info
                part_exists.part_info = part_info
                db.session.commit()
            # else pass
            else:
                pass


        else:
            # 1. Add part number to DB
            new_part = Parts(part_number=part_number,model_id=model_id, part_info=part_info)
            db.session.add(new_part)
            db.session.commit()

        # 2. Make many to many relationship between new part and repair
        # Parts is the parent in this case
        parts = db.session.query(Parts).filter_by(part_number=part_number).first()
        parts.repair_list.append(repair)
        db.session.add(parts)
        db.session.commit()

        # Create our json return object full of parts for this repair:
        parts = get_parts_json(repair)
        inventory = {}
        for part in parts:
            if parts[part]["part_id"] is not None:
                inventory[part] = get_inventories(parts[part]["part_id"])

        # parts = get_parts_json(repair_type)
        return Response(json.dumps([parts, inventory]), mimetype='application/json')

# An example how to add a child to a parent for many to many relationship in sqlalchemy
# p = Parent()
# c = Child()
# p.children.append(c)
# db.session.add(p)
# db.session.commit()



    if request.method == 'DELETE':
        data = request.get_json()["part_number"]
        part_to_delete = db.session.query(Parts).filter_by(part_number=data).first()
        db.session.delete(part_to_delete)
        db.session.commit()


@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_inventory/<path:part_number>", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def get_inventory(part_number):

    # URL decode model_name first:
    part_number = urllib.parse.unquote_plus(part_number)
    print(part_number)

    def get_location_id(part_id):
        location_ids = []

        locations = db.session.query(Inventories).filter_by(part_id=part_id).all()
        for location in locations:
            print(location.location_id)
            # location_ids[location.location_id] = location.location_id
            location_ids.append(location.location_id)
        return location_ids

    def get_location_desc_per_location_id(location_id):
        location_desc = db.session.query(Locations).filter_by(location_id=location_id).first().location_desc
        return location_desc

    def get_inventory(part_id, location_id):
        inventory = db.session.query(Inventories).filter_by(part_id=part_id,location_id=location_id).first()
        return inventory

    def get_part_id(part_number):
        part_id = db.session.query(Parts).filter_by(part_number=part_number).first().part_id
        return part_id

    # This is the messiest way to organize this inventory object. both this and front end need to be redesigned.

    def get_request_inventory():
        part_id = get_part_id(part_number)
        inventory_object = {}
        locations = get_location_id(part_id)
        print(locations)
        for location in locations:
            print(location)
            inventory_by_loc = get_inventory(part_id, location)
            print(inventory_by_loc)
            inventory_object[part_number] = {}
            inventory_object[part_number][location] = {}
            inventory_object[part_number][location]['count'] = inventory_by_loc.count
            inventory_object[part_number][location]['location_desc'] = get_location_desc_per_location_id(location)
        return inventory_object

    if request.method == 'GET':

        inventory_object = get_request_inventory()

        return Response(json.dumps(inventory_object), mimetype='application/json')

    if request.method == 'POST':
        part_id = get_part_id(part_number)
        location_desc = request.get_json()["location_desc"]
        location_id_by_name = db.session.query(Locations).filter_by(location_desc=location_desc).first().location_id
        count = request.get_json()["count"]
        new_inventory = Inventories(count=count, part_id=part_id, location_id=location_id_by_name)
        db.session.add(new_inventory)
        db.session.commit()

        inventory_object = get_request_inventory()

        return Response(json.dumps(inventory_object), mimetype='application/json')

    # Better to use a put or patch method
    if request.method == 'PUT':
        part_id = get_part_id(part_number)
        location_desc = request.get_json()["location_desc"]
        location_id_by_name = db.session.query(Locations).filter_by(location_desc=location_desc).first().location_id
        count = request.get_json()["count"]
        current_inventory = db.session.query(Inventories).filter_by(part_id=part_id).first()
        # Geusing this is a PUT requset: if record exists, then update; if no record found, then create new one.
        if current_inventory is None:
            new_inventory = Inventories(count=count, part_id=part_id, location_id=location_id_by_name)
            db.session.add(new_inventory)
            db.session.commit()
        else:
            current_inventory.count = count
            current_inventory.location_id = location_id_by_name
            db.session.commit()

        inventory_object = get_request_inventory()

        return Response(json.dumps(inventory_object), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/use_part/<part_number>", methods = ['PATCH'])
def use_part(part_number):
    # Need to convert the URL encoded string, part_number, to UTF-8, so we can query the DB!
    part_number = urllib.parse.unquote(part_number)

    if request.method == 'PATCH':
        part_id = db.session.query(Parts).filter_by(part_number=part_number).first().part_id
        current_inventory = db.session.query(Inventories).filter_by(part_id=part_id).first()
        # Geusing this is a PUT requset: if record exists, then update; if no record found, then create new one.

        if current_inventory is not None:
            if current_inventory.count == 0:
                return Response(json.dumps({"message": "Count is already zero!"}), mimetype='application/json')
            current_inventory.count -= 1 # Hope this is right syntax
            db.session.commit()


        return Response(json.dumps(current_inventory), mimetype='application/json')
    return Response(json.dumps({"message": "Error: could not deduct one from inventory"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/get_locations/", methods = ['GET', 'POST', 'PATCH'])
def get_locations():
    if request.method == 'GET':
        locations = db.session.query(Locations).all()
        print(locations)
        location_object = {}
        for location in locations:
            location_object[location.location_desc] = {}
            location_object[location.location_desc]["location_id"] = location.location_id
        return Response(json.dumps(location_object), mimetype='application/json')

    if request.method == 'POST':
        location_desc = request.get_json()["location_desc"]
        new_location = Locations(location_desc=location_desc)
        db.session.add(new_location)
        db.session.commit()
        return Response(json.dumps({"message": f"okay: Added {location_desc} to the Locations table"}), mimetype='application/json')

    if request.method == 'PATCH':
        location_desc = request.get_json()["location_desc"]
        location_id = request.get_json()["location_id"]
        current_locations = db.session.query(Locations).filter_by(location_id=location_id).first()
        # Just to reference the old location desc, so I can return it back in response
        old_location_desc = current_locations.location_desc
        current_locations.location_desc = location_desc
        db.session.add(current_locations)
        db.session.commit()
        return Response(json.dumps({"message": f"okay: changed  {old_location_desc} to {location_desc}"}), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/inventory_analysis", methods = ['GET', 'POST'])
def analyse_inventory():

    # Get all inventories that have a count less than 5
    if request.method == 'GET':
        pass
    # Get all inventories that have a certain count or less
    if request.method == 'POST':
        pass

    return None

@app.route(f"/{os.environ.get('API_ROOT_URL')}/receive_parts/<path:part_number>", methods = ['GET', 'POST'])
def receive_parts(part_number):
    # Need to convert the URL encoded string, part_number, to UTF-8, so we can query the DB!
    part_number = urllib.parse.unquote(urllib.parse.unquote(part_number))
    print(part_number)

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        # Get input
        count = request.get_json()["count"]
        location_desc = request.get_json()["location_desc"]
        part_info = request.get_json()["part_info"]

        # Add part if not part_exists
        parts = db.session.query(Parts).filter_by(part_number=part_number).first()

        if parts:
            # continue
            pass
        else:
            # add new part
            new_part = Parts(part_number=part_number, part_info=part_info)
            db.session.add(new_part)
            db.session.commit()

            # Get new part
            parts = db.session.query(Parts).filter_by(part_number=part_number).first()

        # Get part id of new part
        part_id = parts.part_id

        # Get loctions ID
        location_id = db.session.query(Locations).filter_by(location_desc=location_desc).first().location_id

        # Add count to inventory
        # check if inventory exists
        current_inventory = db.session.query(Inventories).filter_by(part_id=part_id).first()
        # Geusing this is a PUT requset: if record exists, then update; if no record found, then create new one.
        if current_inventory is None:
            new_inventory = Inventories(count=count, part_id=part_id, location_id=location_id)
            db.session.add(new_inventory)
            db.session.commit()

            # Get our new inventory
            current_inventory = db.session.query(Inventories).filter_by(part_id=part_id).first()
        else:
            current_inventory.count = count
            current_inventory.location_id = location_id
            db.session.commit()

        # Make object for inventory object
        inventory_object = {}
        inventory_object["count"] = count
        inventory_object["location_id"] = location_id
        inventory_object["location_desc"] = location_desc

        # Make object for parts object
        parts_object = {}
        parts_object["part_number"] = part_number
        parts_object["part_info"] = part_info
        parts_object["part_id"] = part_id

        # Send email notifing of new parts recieved into inventory:
        sender = "toby2494.development@gmail.com"
        recipients = ["toby2494@gmail.com", "jlynn@agirepairtx.com", "lcenteno@agirepairtx.com", "trenfro@agirepairtx.com"]
        for recipient in recipients:
            generate_then_send(app, sender, recipient,f"Received {count} of {part_number} in {location_desc}", f"{part_number} has recently been stocked. \n \n Count: {count} \n Location: {location_desc} ", None)


        # Return new part object and inventory object
        return Response(json.dumps([parts_object, inventory_object]), mimetype='application/json')

@app.route(f"/{os.environ.get('API_ROOT_URL')}/add_part_to_repair_type/", methods = ['GET', 'POST'])
def add_part_to_repair_type():
    # get part_number and repair_type from request.json()
    part_repair_data = (request.get_json()["part_number"], request.get_json()["repair_type"])

    # Get all inventories that have a count less than 5
    if request.method == 'GET':
        pass
    # Get all inventories that have a certain count or less
    if request.method == 'POST':
        pass

    return None

@app.route(f"/{os.environ.get('API_ROOT_URL')}/uploadInventory", methods = ['GET', 'POST'])
def uploadInventory():


    # Get all inventories that have a count less than 5
    if request.method == 'GET':
        pass
    # Get all inventories that have a certain count or less
    if request.method == 'POST':
        # check if the post request has the file part
        if 'myFile' not in request.files:
            return Response(json.dumps({"message": "Error: No File sent"}), mimetype='application/json')
        # get file from request object
        file = request.files['myFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r") as f:
                lines = csv.reader(f)

                for i, line in enumerate(lines):
                    if i == 0:
                        continue
                    part_number = line[0].strip()
                    count = line[1].strip()
                    location = line[2].strip()
                    part_info = line[3].strip()

                    # Query location and get id
                    location_query = db.session.query(Locations).filter_by(location_desc=location).first()

                    # new location, so make a new one
                    if location_query is None:
                        new_location = Locations(location_desc=location)
                        db.session.add(new_location)
                        db.session.commit()
                        # Query location and get id
                        location_query = db.session.query(Locations).filter_by(location_desc=location).first()
                        location_id = location_query.location_id
                    else:
                        location_id = location_query.location_id


                    # Let's skip this for now:
                    # Existing Inventory
                    # inventory at that location and part number exist, then add count to existing inventory

                    # If part_number not is db, make new part_number:
                    part_query = db.session.query(Parts).filter_by(part_number=part_number).first()

                    if part_query is None:
                        # add new part
                        new_part = Parts(part_number=part_number, part_info=part_info)
                        db.session.add(new_part)
                        db.session.commit()
                        part_query = db.session.query(Parts).filter_by(part_number=part_number).first()
                        part_id = part_query.part_id
                    else:
                        part_id = part_query.part_id

                    # Add new inventory
                    new_inventory = Inventories(count=count, part_id=part_id, location_id=location_id)
                    db.session.add(new_inventory)
                    db.session.commit()

            # file_extension = os.path.splitext(file.filename)[1]
            # if file_extension == "csv":
            #
            # else:
            #     # Program to extract a particular row value
            #
            #     loc = ("path of file")
            #
            #     wb = xlrd.open_workbook(loc)
            #     sheet = wb.sheet_by_index(0)
            #
            #     sheet.cell_value(0, 0)
            #
            #     for row in sheet:
            #         print(sheet.row_values(row))
        else:
            return Response(json.dumps({"message": "File extention not allowed for upload to this server"}), mimetype='application/json')


    return Response(json.dumps({"message": "File sent!"}), mimetype='application/json')


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''





# class Parts(db.Model):
#     __tablename__ = "parts"
#     part_id = db.Column(db.Integer, primary_key=True)
#     part_number = db.Column(db.String, unique=True)
#     alt_part_numbers = db.Column(db.String)
#     model_id = (db.Integer, db.ForeignKey("models.model_id"))
#     repair_id = (db.Integer, db.ForeignKey("repairs.repair_id"))
#
#
# class Locations(db.Model):
#     __tablename__ = "locations"
#     location_id = db.Column(db.Integer, primary_key=True)
#     location_desc = db.Column(db.String, nullable=False, unique=True)
#
# class Inventories(db.Model):
#     __tablename__ = "inventories"
#     inventory_id = db.Column(db.Integer, primary_key=True)
#     count = db.Column(db.Integer, nullable=False)
#     part_id = (db.Integer, db.ForeignKey("parts.part_id"))
#     location_id = (db.Integer, db.ForeignKey("locations.location_id"))
if __name__ == '__main__':
    app.run(debug=True)
