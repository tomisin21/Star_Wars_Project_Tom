import requests
import pymongo
from pprint import pprint

client = pymongo.MongoClient()
db = client['starwars']


def get_starwars_data(api_url='https://swapi.dev/api', keyword='starships', page_number=1, star_wars_data=[]):
    # This function provides a list of all the items within a given category in the swapi database.
    # By creating arguments and providing default arguments for the site api & category values the flexibility
    # of the code is significantly increased.
    # This function is also a recursive function which is operates by providing an iterative index (page_number)
    # which updates the page number in url string.
    # All items found are appended to the star_wars_data list in dict form
    # which by providing a default argument of an empty list
    # ensures it's updated everytime the recursive function is in operation

    url = f"{api_url}/{keyword}/?page={page_number}"  # Forming the URL string from the arguments provided
    response = requests.request("GET", url)


    for result in response.json()['results']:
        star_wars_data.append(result)

    if response.json()['next'] is not None:  # If the value of 'next' contains a url to the next page, do the following:
        page_number += 1  # Updates the page number
        return get_starwars_data(api_url, keyword, page_number, star_wars_data)

    return star_wars_data  # Return the list of items


def get_pilot_info(starship_data):
    # This function replaces the pilot key in a star wars dataset with the name

    for starship in starship_data:
        pilot_data = []
        if starship['pilots']:
            for pilot_url in starship['pilots']:
                response = requests.request("GET", pilot_url)
                pilot_data.append(response.json()['name'])
            starship['pilots'] = pilot_data

    return starship_data



def replace_with_id(starship_data):
    # This function replaces the pilot key in a star wars dataset with the object id
    for starship in starship_data:
        pilot_data = []
        if starship['pilots']:
            for pilot_name in starship['pilots']:
                object_id = db.characters.find_one({'name': pilot_name}, {'_id': 1})
                pilot_data.append(object_id['_id'])
                starship['pilots'] = pilot_data
    return starship_data


def overwrite(collection_name='starships'):
    # User has the option of overwriting their specified collection
    overwrite_prompt = input('Do you wish to overwrite? \'Y\' for Yes, \'N\' for No: ')
    print()

    if overwrite_prompt.upper() == 'Y':
        overwrite = True
    else:
        overwrite = False

    if overwrite:
        return db[collection_name].delete_many({})
    else:
        print('Function to carry on as usual')


def insert_data(dataset, collection_name='starships', overwrite=False):
    # This function uploads a given star wars dataset into a specified collection.

    if overwrite:  # Calling the overwrite function
        return db[collection_name].delete_many({})

    collection_check = []
    for item in dataset:
        db[collection_name].insert_one(item)  # Insert item into specified collection
        collection_check.append(item['name'])  # Returns a list of all the items that have been uploaded
    list_length = len(collection_check)

    pprint(f'Uploaded following dataset: {collection_check} Length: {list_length}')
    print('Function Completed')