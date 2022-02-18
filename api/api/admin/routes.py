import os
from api import app, db, bcrypt
from models import User

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/login")
def login():
    pass

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/logout")
def logout():
    pass

@app.route(f"/{os.environ.get('API_ROOT_URL')}/admin/register")
def logout():
    pass