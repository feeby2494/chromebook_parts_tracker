from api import app
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB')
db = SQLAlchemy(app)

# Thank you Pretty Printed!!! I will need to use automap, so I can update inventory
# brands = db.Table('brands', db.metadata, autoload=True, autoload_with=db.engine)
# repairs = db.Table('repairs', db.metadata, autoload=True, autoload_with=db.engine)
# repairs.repa

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Brands = Base.classes.brands
Models = Base.classes.models
Repairs = Base.classes.repairs
Parts = Base.classes.parts
Inventories = Base.classes.inventories
Locations = Base.classes.locations

# class Brands(db.Model):
#     __tablename__ = "brands"
#     brand_id = db.Column(db.Integer, primary_key=True)
#     brand_name = db.Column(db.String, nullable=False, unique=True)
#
# class Models(db.Model):
#     __tablename__ = "models"
#     model_id = db.Column(db.Integer, primary_key=True)
#     model_name = db.Column(db.String, nullable=False, unique=True)
#     brand_id = (db.Integer, db.ForeignKey("brands.brand_id"))
#
# class Repairs(db.Model):
#     __tablename__ = "repairs"
#     repair_id = db.Column(db.Integer, primary_key=True)
#     repair_type = db.Column(db.String, nullable=False, unique=True)
#     repair_area = db.Column(db.String, nullable=False)
#     model_id = (db.Integer, db.ForeignKey("models.model_id"))
#
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
