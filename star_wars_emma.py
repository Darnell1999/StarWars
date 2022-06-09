import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']

def pilot(url):
    """This function takes the starship API as the input and returns the APIs of the pilots as a list"""
    sw_req = requests.get(url)
    sws = sw_req.json()['pilots']
    return sws


def name(sws):
    """"This functions takes the APIs of the pilots and returns their names as a list"""
    pilot_name = []
    for s in sws:
        pil_req = requests.get(s)
        pil = pil_req.json()['name']
        pilot_name.append(pil)
    return pilot_name


def identify(pilot_name):
    """This function takes the name of the pilots and returns the pilot's object IDs as a list"""
    p_id = []
    for p in pilot_name:
        pilot_id = db.characters.find_one({"name": p}, {"_id": 1})
        pilot_id = pilot_id["_id"]
        p_id.append(pilot_id)
    return p_id


def create_starship(starship_api):
    """This funtion creates a starship in the starship collection with the list of pilot object ids"""
    list_of_pilot_object_ids = identify(name(pilot(starship_api)))
    sw_req = requests.get(starship_api)
    sw_name = sw_req.json()['name']
    db.starships.insert_one({"name": sw_name, "pilots": list_of_pilot_object_ids})
    return db.starships.find_one({"name": sw_name})


print(create_starship("https://swapi.dev/api/starships/10"))
print(create_starship("https://swapi.dev/api/starships/3"))
print(create_starship("https://swapi.dev/api/starships/9"))
print(create_starship("https://swapi.dev/api/starships/12"))



db.starships.drop()
