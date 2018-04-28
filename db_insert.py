from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.cache

def insert_username(screen_name):
    users = db.users
    users.insert_one({'screen_name': screen_name})

def insert_city(city):
    users = db.users
    users.insert_one({'recent_search': city})

def insert_results(city, videos):
    youtube_search = db.youtube_search
    youtube_search.insert_many([{"city_name": city, "results": videos}])


def cityExists(city):
    youtube_search = db.youtube_search

    if youtube_search.find({"city_name": city}) is None:
        return False
    else:
        True

def getResults(city):
    youtube_search = db.youtube_search

    return youtube_search.find_one({"city_name": city})["results"]

if __name__ == "__main__":
    client = MongoClient()
    db = client.cache

    city = "Boston"
    screen_name = "IrishTechie"

    bostonVideos = {"video0": {"title": "Boston - More Than A Feeling", "image_url": {"url": "https://i.ytimg.com/vi/SSR6ZzjDZ94/default.jpg", "width": 120, "height": 90}, "channel_name": "Tainted Music", "video_id": "SSR6ZzjDZ94"}, "video1": {"title": "Milwaukee Bucks vs Boston Celtics Full Game Highlights / Game 5 / 2018 NBA Playoffs", "image_url": {"url": "https://i.ytimg.com/vi/v89rPk9_Cok/default.jpg", "width": 120, "height": 90}, "channel_name": "MLG Highlights", "video_id": "v89rPk9_Cok"}, "video2": {"title": "Boston Celtics vs Milwaukee Bucks Full Game Highlights / Game 6 / 2018 NBA Playoffs", "image_url": {"url": "https://i.ytimg.com/vi/Mw7IBHdubWo/default.jpg", "width": 120, "height": 90}, "channel_name": "MLG Highlights", "video_id": "Mw7IBHdubWo"}, "video3": {"title": "Boston Celtics vs Milwaukee Bucks - Full Game Highlights | Game 6 | April 26 , 2018 | NBA Playoffs", "image_url": {"url": "https://i.ytimg.com/vi/3le_u1wwLPg/default.jpg", "width": 120, "height": 90}, "channel_name": "Rapid Highlights", "video_id": "3le_u1wwLPg"}, "video4": {"title": "Boston Celtics vs. Milwaukee Bucks Game 6 - April 26, 2018", "image_url": {"url": "https://i.ytimg.com/vi/GiDkYLz8EME/default.jpg", "width": 120, "height": 90}, "channel_name": "Motion Station", "video_id": "GiDkYLz8EME"}, "video5": {"title": "Boston Celtics vs Milwaukee Bucks - Game 6 - Highlights | April 26, 2018 | 2018 NBA Playoffs", "image_url": {"url": "https://i.ytimg.com/vi/qVGqbvGPH1g/default.jpg", "width": 120, "height": 90}, "channel_name": "House of Highlights", "video_id": "qVGqbvGPH1g"}, "video6": {"title": "Boston Bruins Round 2 Hype", "image_url": {"url": "https://i.ytimg.com/vi/Bd_Ihg5ZZu4/default.jpg", "width": 120, "height": 90}, "channel_name": "Spencer Weeks", "video_id": "Bd_Ihg5ZZu4"}, "video7": {"title": "Boston - Boston (1976) [Full Album]", "image_url": {"url": "https://i.ytimg.com/vi/4zDR5jmCXOg/default.jpg", "width": 120, "height": 90}, "channel_name": "Vynil Library", "video_id": "4zDR5jmCXOg"}, "video8": {"title": "Boston Celtics vs Milwaukee Bucks - 1st Half Highlights | Game 6 | April 26 , 2018 | NBA Playoffs", "image_url": {"url": "https://i.ytimg.com/vi/dDAM9QkVsos/default.jpg", "width": 120, "height": 90}, "channel_name": "Rapid Highlights", "video_id": "dDAM9QkVsos"}}
    insert_username(screen_name)
    insert_results(city, bostonVideos)

    print(db.users.find_one({}))
    print(getResults("Boston"))
