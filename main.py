import pymongo
from pprint import pprint

client = pymongo.MongoClient()
db = client['starwars']

luke = db.characters.find_one({'name': 'Luke Skywalker'})

# pprint(list(luke.keys()))

darth_vader = db.characters.find_one({'name': "Darth Vader"}, {'name':1, 'height':1, '_id':0})
pprint(darth_vader)
print()

yellow_eyes = db.characters.find({'eye_color': "yellow"}, {'name':1, '_id':0})
for character in yellow_eyes:
    pprint(character['name'])
print()

male_characters = db.characters.find({'gender':'male'}, {'name':1, '_id':0}).limit(3)
# pprint(list(male_characters))
for character in male_characters:
    pprint(character)
print()

alderaan_natives = db.characters.find({'homeworld.name': 'Alderaan'}, {'name': 1, '_id': 0})
for native in alderaan_natives:
    print(native)

avg_female_height = db.characters.aggregate([
    {'$match': {'gender': 'female'}},
    {'$group': {'_id': "", 'avg_height': {'$avg': '$height'}}}
    ])

print(avg_female_height.next())

