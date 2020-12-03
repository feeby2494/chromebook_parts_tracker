#! /usr/bin/env python3
import sqlite3
from sqlite3 import Error
import json
import os

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to DB sucessfull")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query was executed sucessfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_json_from_file(json_file):
    with open(json_file, "r") as jsonf:
        chromebook_parts = json.load(jsonf)
    jsonf.close()
    return chromebook_parts

def create_all_tables(connection):
    create_tables = [
        """
            CREATE TABLE IF NOT EXISTS brands (
                brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT NOT NULL UNIQUE
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS models (
                model_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL UNIQUE,
                brand_id INTEGER,
                FOREIGN KEY(brand_id) REFERENCES brands(brand_id)
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS repairs (
                repair_id INTEGER PRIMARY KEY AUTOINCREMENT,
                repair_type TEXT NOT NULL UNIQUE,
                repair_area TEXT NOT NULL,
                model_id INTEGER,
                FOREIGN KEY(model_id) REFERENCES models(model_id)
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS parts (
                part_id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT UNIQUE,
                alt_part_numbers TEXT,
                model_id INTEGER,
                repair_id INTEGER,
                FOREIGN KEY(model_id) REFERENCES models(model_id),
                FOREIGN KEY(repair_id) REFERENCES repairs(repair_id)
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS locations (
                location_id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_desc TEXT NOT NULL UNIQUE
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS inventories (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER NOT NULL,
                part_id INTEGER,
                location_id INTEGER,
                FOREIGN KEY(part_id) REFERENCES parts(part_id),
                FOREIGN KEY(location_id) REFERENCES locations(location_id)
            );
        """
    ]
    for query in create_tables:
        execute_query(connection, query)

def add_brand_to_brands_table(brand_to_add):
    create_brand = """
    INSERT INTO
      brands (brand_name)
    VALUES
      ("{}");
    """.format(brand_to_add)
    print(create_brand)

    execute_query(connection, create_brand)

def add_model_to_models_table(model_name, brand_id):
    create_model = """
    INSERT INTO
      models (model_name, brand_id)
    VALUES
      ("{}", "{}");
    """.format(model_name, brand_id)

    execute_query(connection, create_model)

def add_repair_to_repairs_table(repair_type, repair_area, model_id):
    create_repair = """
    INSERT INTO
      repairs (repair_type, repair_area, model_id)
    VALUES
      ("{}", "{}", "{}");
    """.format(repair_type, repair_area, model_id)

    execute_query(connection, create_repair)

def add_part_to_parts_table(part_number, alt_part_numbers, model_id, repair_id):
    create_part = """
    INSERT INTO
      parts (part_number, alt_part_numbers, model_id, repair_id)
    VALUES
      ("{}", "{}", "{}", "{}");
    """.format(part_number, alt_part_numbers, model_id, repair_id)

    execute_query(connection, create_part)

def add_location_to_locations_table(location_desc):
    create_location = """
    INSERT INTO
      locations (location_desc)
    VALUES
      ("{}");
    """.format(location_desc)

    execute_query(connection, create_location)

def add_inventory_to_inventories_table(count, part_id, location_id):
    create_inventory = """
    INSERT INTO
      inventories (count, part_id, location_id)
    VALUES
      ("{}", "{}", "{}");
    """.format(count, part_id, location_id)

    execute_query(connection, create_inventory)

def add_brands_to_db(list_of_brands):
    for brand in list_of_brands:
        add_brand_to_brands_table(brand)

# Selecting Records:
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def get_brands_from_db():
    select_brands_from_db = "SELECT * from brands"
    brands_from_db = execute_read_query(connection, select_brands_from_db)
    for brand in brands_from_db:
        print(brand)

def get_models_from_db():
    select_models_from_db = "SELECT * from models"
    models_from_db = execute_read_query(connection, select_models_from_db)
    for model in models_from_db:
        print(model)

def get_repairs_from_db():
    select_repairs_from_db = "SELECT * from repairs"
    repairs_from_db = execute_read_query(connection, select_repairs_from_db)
    for repair in repairs_from_db:
        print(repair)

def get_parts_from_db():
    select_parts_from_db = "SELECT * from parts"
    parts_from_db = execute_read_query(connection, select_parts_from_db)
    for part in parts_from_db:
        print(part)

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

if __name__ == "__main__":
    # Connect to db
    connection = create_connection("./chromebook_inventory.sqlite")

    # create all our tables
    create_all_tables(connection)

    # We need to get our json file and import as dictionary
    chromebook_parts = create_json_from_file("../chromebook_parts_parser/chromebook_parts.json")

    # define some vars to make parsing easier
    brands_list = chromebook_parts["brands"].keys()



    # Adding brands to DB
    for brand in brands_list:
        add_brand_to_brands_table(brand)
    # We need to select brands from DB to get brand_ids


    # add models for each brand
    for brand in brands_list:
        for model in chromebook_parts["brands"][brand]:
            if model == None or model == " " or model == "":
                continue
            add_model_to_models_table(model, get_brand_id(brand))
            print(f"{model} added to db to models table\n brand is linked to {brand}\n")
            for repair in chromebook_parts["brands"][brand][model]:
                if repair == None or repair == " " or repair == "":
                    continue
                add_repair_to_repairs_table(repair, chromebook_parts["brands"][brand][model][repair]["assembly"], get_model_id(model))
                print(f"\t{repair} is a repair for model: {model}")
                for part in chromebook_parts["brands"][brand][model][repair]["parts"]:
                    if part == None or part == " " or part == "" or part == "N/A".upper():
                        continue
                    add_part_to_parts_table(part, 'none', get_model_id(model), get_repair_id(repair))
                    print(f"\t\t{part} is a part for {repair}")
    print("Brands: ")
    get_brands_from_db()
    print("Models: ")
    get_models_from_db()
    print("Repairs: ")
    get_repairs_from_db()
    print("Parts: ")
    get_parts_from_db()
