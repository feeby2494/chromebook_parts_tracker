#!/usr/bin/env python3

import csv
import os
from datetime import date


# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

import sys
sys.path.append('..')
from api.__init__ import app
from api.emails import generate_then_send, send

# Let's get cyma csv and build array of objects

cyma_inv = []

with open(sys.argv[1], 'r') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        line_obj = {}
        line_obj["part_number"] = line[0]
        line_obj["cyma_count"] = line[1]
        cyma_inv.append(line_obj)

f.close()



# Let's get physcial CSV and build array of objects

phy_inv = []

with open(sys.argv[2], 'r') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        line_obj = {}
        line_obj["part_number"] = line[0]
        line_obj["phy_count"] = line[1]
        phy_inv.append(line_obj)

f.close()

# # Let's make the csv file
with open(f'all_inventory_{date.today()}.csv', 'w') as f:
    csv_w = csv.writer(f)
    csv_w.writerow(["part_number", "cyma_count", "physical_count"])

    for cyma_row in cyma_inv:
        print(cyma_row)
        line_obj = [cyma_row["part_number"], cyma_row["cyma_count"], 0]
        for phy_row in phy_inv:
            if cyma_row["part_number"] == phy_row["part_number"]:
                line_obj = [cyma_row["part_number"], cyma_row["cyma_count"], phy_row["phy_count"]]
        csv_w.writerow(line_obj)
            
                
        

f.close()

# # I need this csv file emailed to me:
# sender = "toby2494.development@gmail.com"
# recipients = ["toby2494@gmail.com", "jlynn@agirepairtx.com"]
# subject = f'All Inventory including CB, MB, and iPads as of: {date.today()}'
# body = f"Here's the current inventory as of: {date.today()}\n in csv format"
# attachment_path = f'inventory_cb_mb_{date.today()}.csv'
# for recipient in recipients:
#     generate_then_send(app, sender, recipient, subject, body, attachment_path)