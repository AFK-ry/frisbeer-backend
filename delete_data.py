import os
import sys

'''
    Simply deletes all data from tables
'''

sys.path.append(os.path.join(os.path.dirname(__file__), 'djangofiles'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "server.settings")

import django
django.setup()
from frisbeer.models import *

Game.objects.all().delete()
Player.objects.all().delete()
Season.objects.all().delete()
Location.objects.all().delete()
GamePlayerRelation.objects.all().delete()
Team.objects.all().delete()
