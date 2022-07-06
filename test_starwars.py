from starwars_api_classes import *
import unittest



class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        self.star_wars1 = Starwars()


    def test_generate_url(self):
        self.assertEqual(self.star_wars1.generate_url_string(), 'https://swapi.dev/api/starships/?page=1',
                         'Expected to generate the url string https://swapi.dev/api/starships/?page=1')


    def test_get_starwars_data(self):
        actual = self.star_wars1.get_starwars_data()
        self.assertEqual(len(actual), 36, 'Expected to produce a list with 36 items')
        self.assertEqual(actual[4]['pilots'][0][:5], 'https', 'The pilot values should start with https')

    def test_get_pilot_info(self):
        actual = self.star_wars1.get_pilot_info()
        self.assertEqual(len(actual), 36, 'Expected to produce a list with 36 items')
        self.assertNotEqual(actual[4]['pilots'][0][:5], 'https', 'The pilot key should differ from the original dataset')

    def test_replace_with_id(self):
        actual = self.star_wars1.replace_with_id()
        id_length = len(str(actual[4]['pilots'][0]))
        test_pilot_list = actual[4]['pilots']
        self.assertEqual(len(actual), 36, 'Expected to produce a list with 36 items')
        for pilot in test_pilot_list:
            self.assertEqual(len(str(pilot)), id_length, 'The pilot key should be 24 characters')





# star_wars1 = Starwars()
# dataset = star_wars1.get_starwars_data()
# pprint(dataset)



if __name__ == '__main__':
    unittest.main()