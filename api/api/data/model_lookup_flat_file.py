#!/usr/bin/env python3

import csv
from dotenv import load_dotenv
import os

# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

import sys
sys.path.append('../..')
from api.__init__ import app
from api.models.chromebook_inventory import db, Brands, Models, Repairs, Parts, Inventories, Locations

load_dotenv()



# We are acessing test db outside of the flask framework here:
# Need to use automap and reflecting because we already created the tables!
# Base = automap_base()
# db = os.environ.get('DB_TEST_FOR_CSV_TO_DB_SCRIPT')
# engine = create_engine(db)
#
#
# # reflect the tables
# Base.prepare(engine, reflect=True)
#
# # mapped classes are now created with names by default
# # matching that of the table name.
# Brands = Base.classes.brands
# Models = Base.classes.models
# Repairs = Base.classes.repairs
# Parts = Base.classes.parts
# Inventories = Base.classes.inventories
# Locations = Base.classes.locations
#
# session = Session(engine)

def build_from_db_dic():
    dic = {}
    brands = db.session.query(Brands).all()

    for brand in brands:
        if brand.brand_id:
            brand_id_for_brand = brand.brand_id
            dic[brand.brand_name] = {}
            models = db.session.query(Models).filter_by(brand_id=brand_id_for_brand).all()
            dic[brand.brand_name]["models"] = {}
            for model in models:
                dic[brand.brand_name]["models"][model.model_name] = {}
                model_id_for_model = model.model_id
                repairs = db.session.query(Repairs).filter_by(model_id=model_id_for_model).all()
                dic[brand.brand_name]["models"][model.model_name]["repairs"] = {}
                for repair in repairs:
                    dic[brand.brand_name]["models"][model.model_name]["repairs"][repair.repair_type] = {}
                    repair_id_for_repair = repair.repair_id
                    parts = db.session.query(Parts).filter_by(repair_id=repair_id_for_repair).all()
                    dic[brand.brand_name]["models"][model.model_name]["repairs"][repair.repair_type]["parts"] = {}
                    for part in parts:
                        dic[brand.brand_name]["models"][model.model_name]["repairs"][repair.repair_type]["parts"][part.part_number] = part.part_number


    return dic

def build_flat_dic(dic):
    """

            Let's build the flat dictionary for part_number : Model_name

    """
    flat_dic = {}

    for brand in dic:
        for model in dic[brand]["models"]:
            flat_dic[model] = []
            for repair in dic[brand]["models"][model]["repairs"]:
                for part in dic[brand]["models"][model]["repairs"][repair]["parts"]:
                    flat_dic[model].append(part)
    return flat_dic

def build_csv(dic):
    with open("flat_parts.csv", "w") as f:
        csv_writer = csv.writer(f)
        for item in dic:
            temp = []
            temp.append(item)
            for part in dic[item]:
                temp.append(part)
            csv_writer.writerow(temp)
    f.close()

if __name__ == "__main__":
    dictionary_not_flat = build_from_db_dic()

    flat_dic = build_flat_dic(dictionary_not_flat)

    build_csv(flat_dic)
