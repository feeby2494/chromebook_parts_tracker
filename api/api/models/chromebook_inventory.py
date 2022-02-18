import os
from api import app, db, migrate
from flask_sqlalchemy  import SQLAlchemy
# from sqlalchemy.ext.automap import automap_base


# manager = Manager(app)
#
# manager.add_command('db', MigrateCommand)

# Thank you Pretty Printed!!! I will need to use automap, so I can update inventory
# brands = db.Table('brands', db.metadata, autoload=True, autoload_with=db.engine)
# repairs = db.Table('repairs', db.metadata, autoload=True, autoload_with=db.engine)
# repairs.repa

# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Brands = Base.classes.brands
# Models = Base.classes.models
# Repairs = Base.classes.repairs
# Parts = Base.classes.parts
# Inventories = Base.classes.inventories
# Locations = Base.classes.locations


# I really don't have the sightest clue why this doen't work.
# I really need this many-to-many relationship for my app the work.

part_repair_association = db.Table('part_repair_association',
    db.metadata,
    db.Column('part_id', db.Integer, db.ForeignKey("parts.part_id")),
    db.Column('repair_id', db.Integer, db.ForeignKey("repairs.repair_id"))
)


class Parts(db.Model):
    __tablename__ = "parts"
    part_id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String, unique=True)
    alt_part_numbers = db.Column(db.String)
    part_info = db.Column(db.String)
    model_id = db.Column(db.Integer, db.ForeignKey("models.model_id"))
    repair_list = db.relationship("Repairs", secondary=part_repair_association, backref=db.backref("parts", lazy= "dynamic"))

class Repairs(db.Model):
    __tablename__ = "repairs"
    repair_id = db.Column(db.Integer, primary_key=True)
    repair_type = db.Column(db.String, nullable=False, unique=True)
    repair_area = db.Column(db.String, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("models.model_id"))



# Example of many to many
# dogs = db.Table("dogs",
#         db.metadata,
#         db.Column("id", db.Integer, primary_key = True),
#         db.Column("dog_id", db.Integer, db.ForeignKey("dog.id")),
#         db.Column("hippie_id", db.Integer, db.ForeignKey("hippie.id")),
#         )
# unique index of hippie_id and dog_id
# db.Index("love", dogs.c.hippie_id, dogs.c.dog_id, unique = True)
#
# class Hippie(db.Model):
#     """
#     Hippie model contains relationship to "Dog"
#     secondary table "dogs" is "helper" table which contains
#     unique index of Hippie.id and Dog.id
#     the backref "hippies" provides a query object for Dog
#     """
#     __tablename__ = "hippie"
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64), unique=True, nullable=False)
#     dogs = db.relationship("Dog",
#             secondary=dogs,
#             backref=db.backref("hippies", lazy="dynamic"),
#             )
#
# class Dog(db.Model):
#     """
#     Dog table receives backref to "hippies" when a "Hippie" entry is created.
#     """
#     __tablename__ = "dog"
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64), unique=True, nullable=False)

class Brands(db.Model):
    __tablename__ = "brands"
    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, nullable=False, unique=True)

class Models(db.Model):
    __tablename__ = "models"
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String, nullable=False, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.brand_id"))


class Locations(db.Model):
    __tablename__ = "locations"
    location_id = db.Column(db.Integer, primary_key=True)
    location_desc = db.Column(db.String, nullable=False, unique=True)

class Inventories(db.Model):
    __tablename__ = "inventories"
    inventory_id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("parts.part_id"))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))


# if __name__ == '__main__':
#     manager.run()
