#!/usr/bin/env python3

import csv
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# We are acessing test db outside of the flask framework here:
# Need to use automap and reflecting because we already created the tables!
Base = automap_base()
DB = os.environ.get('DB_TEST_FOR_CSV_TO_DB_SCRIPT')
engine = create_engine(DB)


# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Brands = Base.classes.brands
Models = Base.classes.models
Repairs = Base.classes.repairs
Parts = Base.classes.parts
Inventories = Base.classes.inventories
Locations = Base.classes.locations

session = Session(engine)


# Object for parts not in inventory - will need another script to add these
parts_not_in_db = {}

#Iterrating through CSV file:
with open('monthly_inventory.csv', "r+") as f:
	reader = csv.reader(f, delimiter=",")
	for line in reader:
		part_number = line[0].strip()
		line_part = session.query(Parts).filter_by(part_number=part_number).first()
		# Can't find parts in DB
		if line_part is None:
			parts_not_in_db[part_number] = part_number
		# Found in DB, so will check for existing inventory
		else:
			part_id = line_part.part_id
			count = line[1].strip()
			location_desc = line[3].strip()
			location_object = session.query(Locations).filter_by(location_desc=location_desc).first()
			# Location not added to DB yet, so add location with location_desc
			if location_object is None:
				new_location = Locations(location_desc=location_desc)
				session.add(new_location)
				session.commit()
				print(f"added {location_desc} to locations table")
			elif location_object is not None:
				location_id = location_object.location_id
				print(location_id)
			# check if inventory exists for the location_desc and part_number:
			existing_inventory = session.query(Inventories).filter_by(part_id=part_id,location_id=location_id).all()
			if existing_inventory is None:
				add_inventory = Inventories(part_id=part_id, count=count, location_id=location_id)
				session.add(add_inventory)
				session.commit()
				print(f"added {part_number} to inventory table")
			# elif existing_inventory is not None:
			# 	user_approves = input()
			# # before working more on script, checking values
			print(f"part_id:{part_id}" + "\n" + f"count:{count}" + "\n" + f"location_desc:{location_desc}" + '\n' + f"location_id:{location_id}")
			inventory_stats = session.query(Inventories).filter_by(part_id=part_id).all()
			add_inventory = Inventories(part_id=part_id, count=count, location_id=location_id)
			session.add(add_inventory)
			session.commit()
			print(f"added {part_number} to inventory table")
			print(inventory_stats)
