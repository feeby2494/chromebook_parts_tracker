import os
import tempfile
from .data.create_chrombook_inventory_db import get_brand_id, create_connection, execute_query, execute_read_query, get_model_id
from os import environ
import unittest
import pytest

# from flaskr import flaskr
#
# @pytest.fixture
# def client():
# 	db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
# 	flaskr.app.config['TESTING'] = True
#
# 	with flaskr.app.test_client() as client:
# 		with flaskr.init_db()
# 	yield client
#
# os.close(db_fb)
# os.unlink(flaskr.app.config['DATABASE'])

print("Production DB: "format(environ.get('FLASK_DB')))
print("Production DB: "format(environ.get('TEST_DB')))
