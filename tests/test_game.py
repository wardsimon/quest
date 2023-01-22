from quest.core.match import Match
from quest.core.manager import make_team
from quest.knights.exampleAI import team as ExampleTeam

match = Match(red_team=make_team(ExampleTeam),
              blue_team=make_team(ExampleTeam),
              best_of=3)

match.play(speedup=1, show_messages=False)
