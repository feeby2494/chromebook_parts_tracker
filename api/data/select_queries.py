#!/usr/bin/env python3
from create_chrombook_inventory_db import create_connection, execute_read_query

# Connect to db to test
connection = create_connection("./chromebook_inventory.sqlite")

def get_brand_id(brand_name):
    select_brands_from_db = "SELECT brand_id from brands WHERE brand_name='{}'".format(brand_name)
    brand_id = execute_read_query(connection, select_brands_from_db)
    return brand_id[0][0]

def get_model_id(model_name):
    select_model_from_db = "SELECT model_id from models WHERE model_name='{}'".format(model_name)
    model_id = execute_read_query(connection, select_model_from_db)
    return model_id[0][0]

def get_repair_id(repair_type):
    select_repair_from_db = "SELECT repair_id from repairs WHERE repair_type='{}'".format(repair_type)
    repair_id = execute_read_query(connection, select_repair_from_db)
    return repair_id[0][0]

def get_parts_for_repair(repair_name):
    repair_id = get_repair_id(repair_name)
    select_parts_for_repair = "SELECT * FROM parts INNER JOIN repairs ON repairs.repair_id=parts.repair_id WHERE parts.repair_id='{}'".format(repair_id)
    parts_from_db = execute_read_query(connection, select_parts_for_repair)
    for part in parts_from_db:
        print(part)

def get_repairs_for_model(model_name):
    model_id = get_model_id(model_name)
    select_repairs_for_model = "SELECT * FROM repairs INNER JOIN models ON models.model_id=repairs.model_id WHERE repairs.model_id='{}'".format(model_id)
    repairs_from_db = execute_read_query(connection, select_repairs_for_model)
    for repair in repairs_from_db:
        print(repair)

def get_models_for_brand(brand_name):
    brand_id = get_brand_id(brand_name)
    select_models_for_brand = "SELECT * FROM models INNER JOIN brands ON brands.brand_id=models.brand_id WHERE models.brand_id='{}'".format(brand_id)
    models_from_db = execute_read_query(connection, select_models_for_brand)
    for model in models_from_db:
        print(model)

print(get_parts_for_repair("REPAIR-DELL-CB-CB1C13-GLASS"))
print(get_repairs_for_model("Full Unit Repair for Dell CB1C13 (Gen 1)"))
print(get_models_for_brand("dell"))
