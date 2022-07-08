from starwars_api_classes import *
import unittest


class TestUser(unittest.TestCase):


    def setUp(self) -> None:
        self.star_wars1 = Starwars()
        self.star_wars2 = Starwars()
        self.star_wars3 = Starwars()
        self.star_wars4 = Starwars()
        self.test_dataset = self.star_wars2.get_starwars_data()
        self.test_pilot_ids = self.star_wars3.get_pilot_info(self.test_dataset)


    def connect_to_database(self):
        self.starwars_db = pymongo.MongoClient()['starwars']
        return self.starwars_db


    def create_test_dataset(self):
        self.test_dataset = [{'test': 'testing_value',
                              'pilot': 'https://swapi.dev/api/people/13/'}]
        return self.test_dataset


    def test_generate_url(self):
        actual = self.star_wars1.generate_url_string()
        expected = 'https://swapi.dev/api/starships/?page=1'
        message = f'Expected to generate the url string {expected} instead of {actual}'
        self.assertEqual(actual, expected, message)


    def test_get_starwars_data(self):
        actual = self.star_wars1.get_starwars_data()
        actual_len = len(actual)
        expected_len = self.star_wars1.get_item_count()
        message = f'Expected to produce a list with {expected_len} items instead of {actual_len}'
        test_string = actual[4]['pilots'][0][:5]
        self.assertEqual(actual_len, expected_len, message)
        self.assertEqual(test_string, 'https', 'The pilot values should start with https')


    def test_get_pilot_info(self):
        actual = self.star_wars2.get_pilot_info(self.test_dataset)
        actual_len = len(actual)
        expected_len = self.star_wars2.get_item_count()
        actual_test_string = actual[4]['pilots'][0][:5]
        self.assertEqual(len(actual), expected_len, f'Expected to produce a list with {expected_len} items instead of {actual_len}')
        self.assertNotEqual(actual_test_string, 'https', 'The pilot key should differ from the original dataset')

    def test_replace_with_id(self):
        actual = self.star_wars3.replace_with_id(self.test_pilot_ids)
        id_length = len(str(actual[4]['pilots'][0]))
        test_pilot_list = actual[4]['pilots']
        for pilot in test_pilot_list[:2]:
            self.assertEqual(len(str(pilot)), id_length, 'The pilot key should be 24 characters')

    def test_insert_data(self):
        self.star_wars4.insert_data(self.create_test_dataset(), overwrite=False)
        starwars_db = self.connect_to_database()
        test_dataset = self.create_test_dataset()[0]
        test_query = starwars_db.starships.find_one({'test': 'testing_value'}, {'_id': 0})
        if self.assertEqual(test_query, test_dataset):
            self.starwars_db.starships.delete_one({'test': 'testing_value'})
            print('Test carried out successfully')
        else:
            print('Test carried out unsuccessfully')




if __name__ == '__main__':
    unittest.main()