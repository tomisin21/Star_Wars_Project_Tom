import requests
import pymongo
from pprint import pprint


# client = pymongo.MongoClient()
# db = client['starwars']


class Starwars:

    def __init__(self, api_url='https://swapi.dev/api', keyword='starships', page_number=1, star_wars_data=None):
        if star_wars_data is None:
            star_wars_data = []
        self.api_url = api_url
        self.keyword = keyword
        self.page_number = page_number
        self.star_wars_data = star_wars_data
        self.db = pymongo.MongoClient()['starwars']

    def generate_url_string(self):
        url = f"{self.api_url}/{self.keyword}/?page={self.page_number}"  # Forming the URL string from the arguments provided
        return url

    def get_starwars_data(self):
        # This function provides a list of all the items within a given category in the swapi database.
        # By creating arguments and providing default arguments for the site api & category values, the flexibility
        # of the code is significantly increased.
        # This function is also a recursive function which operates by providing an iterative index (page_number)
        # which updates the page number in url string.
        # All items found are appended to the star_wars_data list in dict form
        # which by providing a default argument of an empty list
        # ensures it's updated everytime the recursive function is in operation

        response = requests.request("GET", self.generate_url_string())

        for result in response.json()['results']:
            self.star_wars_data.append(result)

        if response.json()['next'] is not None:  # If the value of 'next' contains a url to the next page, do the following:
            self.page_number += 1  # Updates the page number
            return self.get_starwars_data()

        return self.star_wars_data  # Return the list of items


    def get_item_count(self):
        response = requests.request("GET", self.generate_url_string())
        count = int(response.json()['count'])
        return count


    def get_pilot_info(self, starship_data, key_item='pilots'):
        # This function replaces the pilot key in a star wars dataset with the name
        for starship in starship_data:
            pilot_data = []
            if starship[key_item]:
                for pilot_url in starship[key_item]:
                    response = requests.request("GET", pilot_url)
                    pilot_data.append(response.json()['name'])
                starship[key_item] = pilot_data

        return starship_data

    def replace_with_id(self, starship_data):
        # This function replaces the pilot key in a star wars dataset with the object id

        for starship in starship_data:
            pilot_data = []
            if starship['pilots']:
                for pilot_name in starship['pilots']:
                    object_id = self.db.characters.find_one({'name': pilot_name}, {'_id': 1})
                    pilot_data.append(object_id['_id'])
                    starship['pilots'] = pilot_data
        return starship_data


    def overwrite(self, collection_name='starships'):
        # User has the option of overwriting their specified collection
        overwrite_prompt = input('Do you wish to overwrite? \'Y\' for Yes, \'N\' for No: ')
        print()

        if overwrite_prompt.upper() == 'Y':
            overwrite = True
        else:
            overwrite = False

        if overwrite:
            return self.db[collection_name].delete_many({})
        else:
            print('Function to carry on as usual')


    def insert_data(self, dataset, overwrite=True):
        # This function uploads a given star wars dataset into a specified collection.

        if overwrite:  # Calling the overwrite function
            self.db[self.keyword].delete_many({})

        total_items_uploaded = 0
        collection_check = []
        for item in dataset:
            self.db[self.keyword].insert_one(item)  # Insert item into specified collection
            total_items_uploaded += 1
        #     collection_check.append(item['name'])  # Returns a list of all the items that have been uploaded
        # list_length = len(collection_check)
        # pprint(f'Uploaded following dataset: {collection_check} Length: {list_length}')
        # print('Function Completed')
        return total_items_uploaded
