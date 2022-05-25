#!/usr/bin/env python3

import csv
from dotenv import load_dotenv
import os
from datetime import date


# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

import sys
sys.path.append('..')
from api.__init__ import app
from api.models.chromebook_inventory import db, Brands, Models, Repairs, Parts, Inventories, Locations
from api.emails import generate_then_send, send

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if not "sqlite:///" in os.environ.get('FLASK_DB'):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/chromebook_inventory.sqlite"
    app.config['SECRET_KEY'] = '\xc6!\xffv[\x9dN\xd8\x1fe\tT\xc8\xeeM\x95\xc4\xbcE]EU[\x92'

# Let's build our list of dics for the csv file we are building

inv = Inventories.query.all()
list_for_csv = []
for i in inv:
    i_obj = []
    part_number = Parts.query.filter_by(part_id = i.part_id).first().part_number
    location_desc = Locations.query.filter_by(location_id = i.location_id).first().location_desc
    i_obj["part_number"] = part_number
    i_obj["count"] = i.count
    i_obj["location_desc"] = location_desc
    list_for_csv.append(i_obj)

print(list_for_csv)

# Let's make the csv file
with open(f'inventory_cb_mb_{date.today()}.csv', 'w') as f:
    csv_w = csv.writer(f)
    csv_w.writerow(["part_number", "count", "location_desc"])

    for row in list_for_csv:
        csv_w.writerow(row.values())

f.close()

# I need this csv file emailed to me:
sender = "toby2494.development@gmail.com"
recipients = ["toby2494@gmail.com", "jlynn@agirepairtx.com"]
subject = f'CB/MB Inventory as of: {date.today()}'
body = f"Here's the current inventory as of: {date.today()}\n in csv format"
attachment_path = f'inventory_cb_mb_{date.today()}.csv'
for recipient in recipients:
    generate_then_send(app, sender, recipient, subject, body, attachment_path)