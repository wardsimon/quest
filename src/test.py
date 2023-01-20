from Quest.core.match import Match
from Quest.core.manager import make_team
from Quest.knights.templateAI import team as TemplateTeam

match = Match(red_team=make_team(TemplateTeam),
              blue_team=make_team(TemplateTeam),
              best_of=3)

match.play(speedup=1, show_messages=False)
