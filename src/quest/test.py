from main import start_match

from neilAI import team as NeilTeam
from madsAI import team as MadsTeam

red_team = ('Neil', [(key, ai) for key, ai in NeilTeam.items()])
blue_team = ('Mads', [(key, ai) for key, ai in MadsTeam.items()])

start_match(red_team=red_team, blue_team=blue_team, speedup=1.0)
