#!/usr/bin/env python3

import csv
import os
from datetime import date


# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

import sys
# sys.path.append('..')
# from api.__init__ import app
# from api.emails import generate_then_send, send

# Let's get all parts from devices not invoiced yet

array_of_counts_to_add = []

with open(sys.argv[1], 'r') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        if line[15] == "TX":
            array_of_counts_to_add.append(line[22])
    

f.close()

# Let's get all these parts counted up in an dic

dic_of_part_counts = {}
for item in array_of_counts_to_add:
    if item in dic_of_part_counts:
        dic_of_part_counts[item] += 1
        
    else:
        dic_of_part_counts[item] = 1
        

print(dic_of_part_counts)

# Get current inv from csv (with cyma inv already added)

inv = []

with open(sys.argv[2], 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for line in csv_reader:
        line_obj = {}
        line_obj["part_number"] = line[0]
        line_obj["cyma_count"] = line[1]
        line_obj["physical_count"] = line[2]
        inv.append(line_obj)

f.close()



# # Let's make the csv file
with open(f'all_inventory_with_devices_not_shipped_{date.today()}.csv', 'w') as f:
    csv_w = csv.writer(f)
    csv_w.writerow(["part_number", "cyma_count", "physical_count"])

    for line in inv:
        line_obj = [line["part_number"], line["cyma_count"], line["physical_count"]]
        for part in dic_of_part_counts:
            if part != '' and part is not None:
                if line["part_number"] == part:
                    print(part, line["cyma_count"], line["physical_count"], dic_of_part_counts[part])
                    new_phy_count = int(line["physical_count"]) + int(dic_of_part_counts[part])
                    line_obj = [line["part_number"], line["cyma_count"], new_phy_count]
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
