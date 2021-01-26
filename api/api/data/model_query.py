from dotenv import load_dotenv
load_dotenv()
import os
from flask_sqlalchemy import SQLAlchemy
from api import app

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLITE_DB')
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Brands(db.Model):
    __tablename__ = db.Model.metadata.tables['brands']

    def __repr__(self):
        return '<title %r>' % self.title

def get_brands():
    print(Brands.query.all())
