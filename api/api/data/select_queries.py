#!/usr/bin/env python3
from .create_chromebook_inventory_db import create_connection, execute_read_query
from dotenv import load_dotenv
import os

load_dotenv()

def get_brand_id(connection, brand_name):
    select_brands_from_db = "SELECT brand_id from brands WHERE brand_name='{}'".format(brand_name)
    brand_id = execute_read_query(connection, select_brands_from_db)
    return brand_id[0][0]

def get_model_id(connection, model_name):
    select_model_from_db = "SELECT model_id from models WHERE model_name='{}'".format(model_name)
    model_id = execute_read_query(connection, select_model_from_db)
    return model_id[0][0]

def get_repair_id(connection, repair_type):
    select_repair_from_db = "SELECT repair_id from repairs WHERE repair_type='{}'".format(repair_type)
    repair_id = execute_read_query(connection, select_repair_from_db)
    return repair_id[0][0]

def get_parts_for_repair(connection, repair_name):
    repair_id = get_repair_id(connection, repair_name)
    select_parts_for_repair = "SELECT * FROM parts INNER JOIN repairs ON repairs.repair_id=parts.repair_id WHERE parts.repair_id='{}'".format(repair_id)
    parts_from_db = execute_read_query(connection, select_parts_for_repair)
    for part in parts_from_db:
        print(part)
    #parts_dictionary = {}
    #for part in parts_from_db:
    #    parts_dictionary[part[1]] = {part_id: part[0], part_number: part[1], model_id: part[3], }
    #return parts_from_db

def get_repairs_for_model(connection, model_name):
    model_id = get_model_id(connection, model_name)
    select_repairs_for_model = "SELECT * FROM repairs INNER JOIN models ON models.model_id=repairs.model_id WHERE repairs.model_id='{}'".format(model_id)
    repairs_from_db = execute_read_query(connection, select_repairs_for_model)
    repairs_dict = {}
    for repair in repairs_from_db:
        repairs_dict[repair[1]] = {}
        repairs_dict[repair[1]]["repair_id"] = repair[0]
        repairs_dict[repair[1]]["repair_type"] = repair[1]
        repairs_dict[repair[1]]["repair_area"] = repair[2]
        repairs_dict[repair[1]]["model_id"] = repair[3]
        repairs_dict[repair[1]]["model_name"] = repair[5]
        repairs_dict[repair[1]]["brand_id"] = repair[6]
    return repairs_dict

def get_models_for_brand(connection, brand_name):
    brand_id = get_brand_id(connection, brand_name)
    select_models_for_brand = "SELECT * FROM models INNER JOIN brands ON brands.brand_id=models.brand_id WHERE models.brand_id='{}'".format(brand_id)
    models_from_db = execute_read_query(connection, select_models_for_brand)
    for model in models_from_db:
        print(model)

if __name__ == "__main__":

    # Connect to db to test
    connection = create_connection(os.environ.get("FLASK_DB"))

    print(get_parts_for_repair(connection, "REPAIR-DELL-CB-CB1C13-GLASS"))
    print(get_repairs_for_model(connection, "Full Unit Repair for HP 11 X360 G1 EE"))
    print(get_models_for_brand(connection, "dell"))
