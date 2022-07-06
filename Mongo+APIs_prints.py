from starwars_functions import *


print('<--------------------------- 1. Printing data retrieved from swapi --------------------------->')
starships = get_starwars_data('https://swapi.dev/api/', 'starships')
pprint(starships)
print()
print('---------------------------------------------------------------------------------------------------')
print()
print('<-------------------------- 2. Printing data with pilot values replaced with names -------------------------->')
refined_starships = get_pilot_info(starships)
pprint(refined_starships)
print()
print('---------------------------------------------------------------------------------------------------')
print()
print('<-------------------------- 3. Printing data with pilot values replaced with ID\'s -------------------------->')
starships_id = replace_with_id(refined_starships)
pprint(starships_id)
print()
print('---------------------------------------------------------------------------------------------------')
print()
print('<-------------------------- 4. Inserting data into specified collection on MongoDB -------------------------->')
insert_data(starships_id)