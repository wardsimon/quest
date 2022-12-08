import sys

sys.path.extend(['core', 'participants'])

from match import Match
from manager import Participant
from neilAI import team as NeilTeam
from madsAI import team as MadsTeam

red_team = ('Neil', NeilTeam)
blue_team = ('Mads', MadsTeam)

match = Match(
    red_team={red_team[0]: Participant(name=red_team[0], knights=red_team[1])},
    blue_team={
        blue_team[0]: Participant(name=blue_team[0], knights=blue_team[1])
    })

match.play(speedup=1)
