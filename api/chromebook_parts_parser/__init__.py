#! /usr/bin/env python3
import os
import csv
import json

def create_dic_for_one_brand(file_to_open):
    parts_dic = {}
    repair_type = ''
    part_name = ''
    repair_model = ''
    repair_area = ''

    with open(file_to_open) as file:
        parts = csv.reader(file)
        for part in parts:
            if "item" not in part[0]:
                if "Full Unit Repair" in part[1]:
                    repair_model = part[1].strip()
                    print("{} is the repair_model".format(repair_model))
                    if repair_model not in parts_dic:
                        parts_dic[repair_model] = {}
                elif "Display Assembly" in part[1]:
                    repair_area = part[1].strip()
                    print("{} is the repair_area".format(repair_area))
                elif "Topcase Assembly" in part[1]:
                    repair_area = part[1].strip()
                    print("{} is the repair_area".format(repair_area))
                elif "REPAIR" in part[0].strip():
                    repair_type = part[0].strip()
                    print("{} is the repair_type".format(repair_type))
                    parts_dic[repair_model][repair_type] = {}
                    parts_dic[repair_model][repair_type]["parts"] = []
                    parts_dic[repair_model][repair_type]["assembly"] = repair_area
                else:
                    part_name = part[0].strip()
                    if repair_model not in parts_dic:
                        parts_dic[repair_model] = {}
                        parts_dic[repair_model][repair_type] = {}
                        parts_dic[repair_model][repair_type]["parts"] = []
                        parts_dic[repair_model][repair_type]["parts"].append(part_name)
                        parts_dic[repair_model][repair_type]["assembly"] = repair_area
                    elif repair_type not in parts_dic[repair_model]:
                        parts_dic[repair_model][repair_type] = {}
                        parts_dic[repair_model][repair_type]["parts"] = []
                        parts_dic[repair_model][repair_type]["parts"].append(part_name)
                        parts_dic[repair_model][repair_type]["assembly"] = repair_area
                    elif "parts" not in parts_dic[repair_model][repair_type]:
                        parts_dic[repair_model][repair_type]["parts"] = []
                        parts_dic[repair_model][repair_type]["parts"].append(part_name)
                    else:
                        parts_dic[repair_model][repair_type]["parts"].append(part_name)
                        parts_dic[repair_model][repair_type]["assembly"] = repair_area
                    print("{} is the repair_type and {} is a part for this type of repair".format(repair_type, part_name))

        return parts_dic

def create_one_master_dic():
    dell_parts = create_dic_for_one_brand("chromebook_dell_parts.csv")
    hp_parts = create_dic_for_one_brand("chromebook_hp_parts.csv")
    lenovo_parts = create_dic_for_one_brand("chromebook_lenovo_parts.csv")
    samsung_parts = create_dic_for_one_brand("chromebook_samsung_parts.csv")
    acer_parts = create_dic_for_one_brand("chromebook_acer_parts.csv")
    asus_parts = create_dic_for_one_brand("chromebook_asus_parts.csv")
    microsoft_parts = create_dic_for_one_brand("chromebook_microsoft_parts.csv")
    toshiba_parts = create_dic_for_one_brand("chromebook_toshiba_parts.csv")

    all_chromebook_parts = {
        "brands": {
            'dell': dell_parts,
            'hp': hp_parts,
            'lenovo': lenovo_parts,
            'samsung': samsung_parts,
            'acer': acer_parts,
            'asus': asus_parts,
            'microsoft': microsoft_parts,
            'toshiba': toshiba_parts
        }
    }

    return all_chromebook_parts

master_parts_list = create_one_master_dic()

def write_to_json(data):
    with open("./chromebook_parts.json", 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

write_to_json(master_parts_list)
