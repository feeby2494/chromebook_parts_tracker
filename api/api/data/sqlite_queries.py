#!/usr/bin/env python3
# -*- mode: python -*-
from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker, Query


# engine = create_engine(os.environ.get('SQLITE_DB'))
# Base = declarative_base()
# Base.metadata.reflect(engine)
#
# # Add brands to our object:
# def get_brands(db_session):
#     if db_session is None:
#         db_session = scoped_session(sessionmaker(bind=engine))
#     brands_dict = {}
#     brands_dict["brands"] = {}
#     for brand in db_session.query(brands_table.brand_name):
#         name, = brand
#         brands_dict["brands"][name] = {}
#     print(brands_dict)
#     return brands_dict
#
# meta = MetaData()
# meta.reflect(bind=engine)
# brands_table = meta.tables['brands']
# models_table = meta.tables['models']

# class Brands(Base):
#     __table__ = Base.metadata.tables['brands']
#
# class Models(Base):
#     __table__ = Base.metadata.tables['models']

if __name__ == '__main__':
    print(os.environ.get('SQLITE_DB'))
    db_session = scoped_session(sessionmaker(bind=engine))
    # for brand in db_session.query(Brands.brand_name):
    #     print(brand)
    #
    # for model in db_session.query(Models.model_name):
    #     name, = model
    #     print(name)

    get_brands(db_session)
    get_brands(None)
