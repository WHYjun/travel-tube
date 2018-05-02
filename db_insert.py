from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.cache

def insert_username(user_name):
    users = db.users
    if users.count({"user_name": user_name}) == 1:
        pass
    else:
        users.insert_one({'user_name': user_name})

def insert_city(city):
    users = db.users
    users.insert_one({'recent_search': city})

def insert_results(city, videos):
    youtube_search = db.youtube_search
    youtube_search.insert_many([{"city_name": city, "results": videos}])

def cityExists(city):
    youtube_search = db.youtube_search

    if youtube_search.count({"city_name": str(city)}) == 0:
        return False
    else:
        return True

def getResults(city):
    youtube_search = db.youtube_search

    return youtube_search.find_one({"city_name": city})["results"]