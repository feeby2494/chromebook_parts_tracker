#! /usr/bin/env python3
import requests

def post_new_location(new_location_desc):
    # set up post to api for adding new location
    r = requests.post('https://chromebooks.jamielynn.dev/api/get_locations/', data = {"location_desc" : new_location_desc})

    # See in terminal if this is doing anything!
    print(r.url)

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
