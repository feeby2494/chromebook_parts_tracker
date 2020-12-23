#!/usr/bin/env python3
from create_chromebook_inventory_db import create_connection, execute_read_query
from dotenv import load_dotenv
import os
import unittest
from select_queries import get_brand_id, get_model_id, get_repair_id, get_parts_for_repair, get_repairs_for_model, get_models_for_brand

load_dotenv()

# Connect to db to test
connection = create_connection(os.environ.get("TEST_DB"))

class Test_X360_get_repairs_from_x360(unittest.TestCase):
    def test_get_repairs_from_x360(self):
        expected_keys = [
        'REPAIR-HP-11-X360-G1-EE-TOUCHSCREEN',
        'REPAIR-HP-11-X360-G1-EE-CAMERA',
        'REPAIR-HP-11-X360-G1-EE-TOPCOVER',
        'REPAIR-HP-11-X360-G1-EE-HINGESET',
        'REPAIR-HP-11-X360-G1-EE-CABLE-RESEAT',
        'REPAIR-HP-11-X360-G1-EE-LVDS',
        'REPAIR-HP-11-X360-G1-EE-PALMREST',
        'REPAIR-HP-11-X360-G1-EE-TRACKPAD',
        'REPAIR-HP-11-X360-G1-EE-BOTTOMCASE',
        'REPAIR-HP-11-X360-G1-EE-BATTERY',
        'REPAIR-HP-11-X360-G1-EE-POWER-BOARD',
        'REPAIR-HP-11-X360-G1-EE-SPEAKERS',
        'REPAIR-HP-11-X360-G1-EE-IO-BOARD',
        'REPAIR-HP-11-X360-G1-EE-WIFI-CARD',
        'REPAIR-HP-11-X360-G1-EE-MOTHERBOARD',
        'REPAIR-HP-11-X360-G1-EE-MISSING-KEY',
        'REPAIR-HP-11-X360-G1-EE-OS-RESTORE',
        'REPAIR-HP-11-X360-G1-EE-CHARGING-PORT-REMOVAL',
        'REPAIR-HP-11-X360-G1-EE-HPJ-REMOVAL'
        ]
        testcase_brand_name = "hp"
        expected_brand_id = 2
        testcase_model_name = "Full Unit Repair for HP 11 X360 G1 EE"
        expected_model_id = 18
        testcase_first_repair = "REPAIR-HP-11-X360-G1-EE-TOUCHSCREEN"
        expected_first_repair_id = 394
        self.assertEqual(get_brand_id(connection, testcase_brand_name), expected_brand_id)
        self.assertEqual(get_model_id(connection, testcase_model_name), expected_model_id)
        self.assertEqual(get_repair_id(connection, testcase_first_repair), expected_first_repair_id)
        self.assertEqual([ key for key in get_repairs_for_model(connection, testcase_model_name).keys()], expected_keys)

    print(get_repairs_for_model(connection, "Full Unit Repair for HP 11 X360 G1 EE"))
if __name__ == "__main__":



    unittest.main()

    # print(get_parts_for_repair(connection, ))
    # print(get_repairs_for_model(connection, "Full Unit Repair for Dell CB1C13 (Gen 1)"))
    # print(get_models_for_brand(connection, "dell"))
