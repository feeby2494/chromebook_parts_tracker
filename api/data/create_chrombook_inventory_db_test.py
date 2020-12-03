#!/usr/bin/env python3

from create_chrombook_inventory_db import get_brand_id, create_connection, execute_query, execute_read_query

import unittest


#
#   get_brand_id test
#

class Test_get_brand_id_dell(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "dell"
        expected = 1
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_hp(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "hp"
        expected = 2
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_lenovo(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "lenovo"
        expected = 3
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_samsung(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "samsung"
        expected = 4
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_acer(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "acer"
        expected = 5
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_asus(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "asus"
        expected = 6
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_microsoft(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "microsoft"
        expected = 7
        self.assertEqual(get_brand_id(testcase), expected)

class Test_get_brand_id_toshiba(unittest.TestCase):
    def test_get_brand_id(self):
        testcase = "toshiba"
        expected = 8
        self.assertEqual(get_brand_id(testcase), expected)


print(get_parts_for_repair("Full Unit Repair for Acer CB5-132T"))

unittest.main()
