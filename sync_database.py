import os
import sys
import random
import requests
import datetime

from django.db import IntegrityError

'''
 Srcipt to copy games, locations and player stats from production environment using the open api's
'''

sys.path.append(os.path.join(os.path.dirname(__file__), 'djangofiles'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "server.settings")
r = requests.get('http://api.frisbeer.win/API/players')
ExternalPlayers = r.json()
r = requests.get('http://api.frisbeer.win/API/locations')
ExternalLocations = r.json()
r = requests.get('http://api.frisbeer.win/API/games')
ExternalGames = r.json()

import django

django.setup()

from frisbeer.models import *
from django.contrib.auth.models import User
from djangofiles.frisbeer.signals import update_elo, update_score, calculate_ranks, update_team_score

Player.objects.all().delete()
fields = ('id', 'name', 'score', 'rank', 'season_best')
for player in ExternalPlayers:
    temp = Player(name=player["name"], score=1500)
    temp.save()
    
Game.objects.all().delete()
Season.objects.all().delete()
Location.objects.all().delete()
GamePlayerRelation.objects.all().delete()
Team.objects.all().delete()
year = 2017
rules = GameRules.objects.get(id=1)
Srules = SeasonRules.objects.get(id=4)
print("starting season loop")
for i in range(datetime.datetime.now().year - year + 1):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime(year, 12, 31)
    s = Season(id=i+2, name=year, start_date=start, end_date=end, game_rules=rules, rules=Srules)
    s.save()
    year = year + 1
print("starting location loop")
for location in ExternalLocations:
    l = Location(id=location["id"], name=location["name"], longitude=location["longitude"], latitude=location["latitude"])
    l.save()


print("starting game loop")
for game in ExternalGames:
    if game["location"] == None:
        loc = None
    else:
        loc = Location.objects.get(id=game["location"])
    g = Game(name=game["name"], season=Season.objects.get(id=game["season"]), location=loc, date=game["date"],
        team1_score=game["team1_score"], team2_score=game["team2_score"], state=game["state"])
    g.save()
    t1 = [d for d in game["players"] if d['team'] in [1]]
    t2 = [d for d in game["players"] if d['team'] in [2]]
    t0 = [d for d in game["players"] if d['team'] in [0]]
    for player in t1:
        temp = Player.objects.get(name=player["name"])
        GamePlayerRelation(player=temp, game=g, team=1).save()
    for player in t2:
        temp = Player.objects.get(name=player["name"])
        GamePlayerRelation(player=temp, game=g, team=2).save()
    for player in t0:
        temp = Player.objects.get(name=player["name"])
        GamePlayerRelation(player=temp, game=g, team=0).save()

print("updating values")
update_elo()
update_score()
calculate_ranks()
update_team_score()

