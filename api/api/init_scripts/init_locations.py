#! /usr/bin/env python3
import requests
import json

def post_new_location(new_location_desc):
    # set up post to api for adding new location
    r = requests.post('https://chromebooks.jamielynn.dev/api/get_locations', data = json.dumps({"location_desc" : new_location_desc}), headers = {"Content-Type" : "application/json"}, timeout=60)

    # See in terminal if this is doing anything!
    print(r)

def check_if_location_exists_array():
    # set up post to api for adding new location
    r = requests.get('https://chromebooks.jamielynn.dev/api/get_locations/', timeout=60)

    # See in terminal if this is doing anything!
    location_desc_that_exist = r.json().keys()
    return location_desc_that_exist

def build_locations():
    inventory_array = []
    number_of_areas = int(input(f"Choose how many areas in your inventory system: \n"))
    number_of_areas_array = range(1, number_of_areas+1)
    for area in number_of_areas_array:
        number_of_shelves_for_current_area = int(input(f"Choose how many shelves are in this area {area}: \n"))
        number_of_shelves_for_current_area_array = range(1, number_of_shelves_for_current_area+1)
        for shelf in number_of_shelves_for_current_area_array:
            number_of_rows_per_shelf = int(input(f"Choose how many rows are on self {shelf} in area {area}: \n"))
            number_of_rows_per_shelf_array = range(1, number_of_rows_per_shelf+1)
            for row in number_of_rows_per_shelf_array:
                inventory_array.append(f"{area:02}{shelf:03}{row:02}")

    return inventory_array



if __name__ == "__main__":
    inventory_system = build_locations()
    print(inventory_system)

    locations_that_exist_array = check_if_location_exists_array()

    for location in locations_that_exist_array:
        if location in inventory_system:
            inventory_system.remove(location)
            print(f"{location} from inventory_system has been removed. \n")

    print(inventory_system)

    print("Now adding each new location to our inventory_system .... \n \n Please Wait....")

    for new_location in inventory_system:
        post_new_location(new_location)
        print(f"Added {new_location} to inventory_system database")
