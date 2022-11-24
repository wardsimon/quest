from main import start_match

from neilAI import team as NeilTeam
from mads import team as MadsTeam

red_team = ('Neil', NeilTeam)
blue_team = ('Mads', MadsTeam)

start_match(red_team=red_team, blue_team=blue_team, speedup=1.0)
