#!/usr/bin/env python3

from create_chrombook_inventory_db import get_brand_id, create_connection, execute_query, execute_read_query, get_model_id
import os
import unittest
import sys
from dotenv import load_dotenv

load_dotenv()

connection = create_connection(os.environ.get("TEST_DB"))
#
#   get_brand_id test
#

class Test_get_brand_ids(unittest.TestCase):
    def test_get_brand_id_dell(self):
        testcase = "dell"
        expected = 1
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_hp(self):
        testcase = "hp"
        expected = 2
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_lenovo(self):
        testcase = "lenovo"
        expected = 3
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_samsung(self):
        testcase = "samsung"
        expected = 4
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_acer(self):
        testcase = "acer"
        expected = 5
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_asus(self):
        testcase = "asus"
        expected = 6
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_microsoft(self):
        testcase = "microsoft"
        expected = 7
        self.assertEqual(get_brand_id(connection, testcase), expected)
    def test_get_brand_id_toshiba(self):
        testcase = "toshiba"
        expected = 8
        self.assertEqual(get_brand_id(connection, testcase), expected)

class Test_get_model_ids(unittest.TestCase):
    def test_get_CB1C13_model_id(self):
        testcase = "Full Unit Repair for Dell CB1C13 (Gen 1)"
        expected = 1
        self.assertEqual(get_model_id(connection, testcase), expected)
    def test_get_CB1C13_model_id(self):
        testcase = "Full Unit Repair for Dell CB1C13 (Gen 1)"
        expected = 1
        self.assertEqual(get_model_id(connection, testcase), expected)
    def test_get_CB1C13_model_id(self):
        testcase = "Full Unit Repair for Dell CB1C13 (Gen 1)"
        expected = 1
        self.assertEqual(get_model_id(connection, testcase), expected)

print(get_model_id(connection, "Full Unit Repair for Acer CB5-132T"))
print(os.environ.get('FLASK_DB'))

unittest.main()
