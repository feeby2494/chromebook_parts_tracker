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
parts_not_in_db = []

def check_part_exists_in_db(part_name):
	part_in_db = session.query(Parts).filter_by(part_number=part_name).first()
	if part_in_db is None:
		return False
	else:
		return True

# This has sideeffect of adding to parts_not_in_db array!
def add_parts_not_in_db_to_list(part_name, list_parts_not_in_db):
	if check_part_exists_in_db(part_name) is False:
		list_parts_not_in_db.append(part_name)
	return None

def check_inventory_exists_for_part(part_name):
	part_id = session.query(Parts).filter_by(part_number=part_name).first().part_id
	inventory = session.query(Inventories).filter_by(part_id=part_id).first()
	if inventory is None:
		return False
	else:
		return True

def zero_out_inventory():
	inventories = session.query(Inventories).all()
	for inventory in inventories:
		inventory.count = 0
		session.commit()

def final_count_dic(final_count):
	with open('monthly_inventory.csv', "r") as f:
		next(f)
		reader = csv.reader(f, delimiter=",")
		for line in reader:
			csv_count = line[1].strip()
			csv_part_number = line[0].strip()

			add_parts_not_in_db_to_list(csv_part_number, parts_not_in_db)

			if csv_part_number in final_count:
				final_count[csv_part_number]["count"] += int(csv_count)
			else:
				final_count[csv_part_number] = {}
				final_count[csv_part_number]["count"] = int(csv_count)
	return final_count
# Only uncommit this if you want to zero out all current inventories!!!
# zero_out_inventory()

def find_part_id(part_name):
	part_id = session.query(Parts).filter_by(part_number=part_name).first().part_id
	return part_id

# Final object with total sums for parts count
final_count = {}
final_count = final_count_dic(final_count)

for part in final_count:
	if check_part_exists_in_db(part):
		part_id = find_part_id(part)

		if check_inventory_exists_for_part(part):
			inventories = session.query(Inventories).filter_by(part_id=part_id).all()
			for inventory in inventories:
				inventory.count = str(final_count[part]["count"])
				print(f"Inventory count will change to: {inventory.count} for inventory_id: {inventory.inventory_id} for part: {part}")
			session.commit()

				# db_part_instances = session.query(Parts).filter_by(part_number=csv_part_number).all()
				# for db_part_instance in db_part_instances:
		else:
			print(f"need to add {part} to inventory")
			new_inventory = Inventories(location_id="1", count=final_count[part]["count"], part_id=part_id)
			session.add(new_inventory)
			session.commit()



		# for db_part_instance in db_part_instances:
		# 	print(f"{db_part_instance.part_id} : {db_part_instance.part_number}")
		#
		# 	if check_inventory_exists_for_part(db_part_instance.part_number):
		# 		db_part_instance_inventories = session.query(Inventories).filter_by(part_id=db_part_instance.part_id).all()
		# 		for db_part_instance_inventory in db_part_instance_inventories:
		# 			print(f"inventory id: {db_part_instance_inventory.inventory_id} and count: {db_part_instance_inventory.count}")
		#


				# session.commit()
				# print(f"added {part_number} to inventory table")
				# print(inventory_stats)



print(f"These parts are not in database and will need to be added manually: \n \n{parts_not_in_db}")

# print(f"\n \n This is the final count dictionary with all counts added together per part number: \n {final_count}")
