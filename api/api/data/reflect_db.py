#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

print(os.environ.get('FLASK_DB'))

engine = sqlalchemy.create_engine(os.environ.get('FLASK_DB'))
meta = sqlalchemy.MetaData()

Session = sessionmaker(engine)
#
#

brands = sqlalchemy.Table('brands', meta, autoload_with=engine)
models = sqlalchemy.Table('models', meta, autoload_with=engine)
repairs = sqlalchemy.Table('repairs', meta, autoload_with=engine)
parts = sqlalchemy.Table('parts', meta, autoload_with=engine)
inventories = sqlalchemy.Table('inventories', meta, autoload_with=engine)
locations = sqlalchemy.Table('locations', meta, autoload_with=engine)
#

insp = sqlalchemy.inspect(engine)
print(f"brands: {brands}")
print(f"brands: {models}")
print(f"brands: {repairs}")
print(f"brands: {parts}")
print(f"brands: {inventories}")
print(f"brands: {locations}")

# def execute_query(query):
#     with Session(engine) as session:
#         result = session.execute(query)
#     return result
#
# print(execute_query("SELECT brand_name FROM brands"))
# with Session() as session:
#     result = session.query(brands).all()
#     print(result)
