import sys

sys.path.extend(['core', 'participants'])

from match import Match
from manager import make_team
from templateAI import team as TemplateTeam

match = Match(red_team=make_team(TemplateTeam),
              blue_team=make_team(TemplateTeam))

match.play(speedup=1)
