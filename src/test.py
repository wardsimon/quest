import sys

sys.path.extend(['core', 'participants'])

from match import Match
from manager import make_team
from templateAI import team as TemplateTeam

match = Match(red_team=make_team(TemplateTeam),
              blue_team=make_team(TemplateTeam),
              best_of=3)

match.play(speedup=1, show_messages=False)
