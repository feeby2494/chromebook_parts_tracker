import requests

def post_new_location(new_location_desc):
    # set up post to api for adding new location
    r = requests.post('https://chromebooks.jamielynn.dev/api/get_locations/', data = {"location_desc" : new_location_desc})

    # See in terminal if this is doing anything!
    print(r.url)
