from .engine import Engine
from typing import Any
from Quest import IS_NOTEBOOK

class Match:

    def __init__(self,
                 red_team: dict,
                 blue_team: dict,
                 number: int = 1,
                 phase: int = 1,
                 rounds: int = None,
                 manager: Any = None,
                 winner: str = None,
                 best_of: int = 3):
        self.red_team = red_team
        self.blue_team = blue_team
        self.number = number
        self.rounds = [] if rounds is None else rounds
        self.phase = phase
        self.manager = manager
        self.best_of = best_of
        self.first_to = self.best_of // 2 + 1
        self.match_winner = winner

    def to_dict(self) -> dict:
        return {
            'phase': self.phase,
            'red': list(self.red_team.keys()),
            'blue': list(self.blue_team.keys()),
            'rounds': self.rounds,
            'number': self.number,
            'winner': self.match_winner
        }

    def to_string(self) -> str:
        return (f'red={list(self.red_team.keys())} VS '
                f'blue={list(self.blue_team.keys())}')

    def update_scores(self, winner: str):
        self.rounds.append(winner)
        if winner == 'red':
            for p in self.red_team.values():
                p.rounds_won += 1
        elif winner == 'blue':
            for p in self.blue_team.values():
                p.rounds_won += 1

    @property
    def score(self) -> dict:
        s = {'red': 0, 'blue': 0, 'count': len(self.rounds) + 1}
        for r in self.rounds:
            if r is not None:
                s[r] += 1
        return s

    def is_complete(self) -> bool:
        return (self.match_winner
                is not None) or (not (len(self.rounds) < self.best_of))

    def update_winner(self, winning_team: str):
        self.match_winner = winning_team
        if winning_team == 'red':
            for p in self.red_team.values():
                p.matches_won += 1
        elif winning_team == 'blue':
            for p in self.blue_team.values():
                p.matches_won += 1

    def play(self,
             speedup: int = 1,
             safe: bool = False,
             show_messages: bool = False):
        for n in range(len(self.rounds), self.best_of):

            if self.phase == 1:
                red = list(self.red_team.keys())[0]
                blue = list(self.blue_team.keys())[0]
                red_team = [(k, v)
                            for k, v in self.red_team[red].knights.items()]
                blue_team = [(k, v)
                             for k, v in self.blue_team[blue].knights.items()]
            else:
                red_team = []
                for p in self.red_team.values():
                    name = list(p.knights.keys())[0]
                    red_team.append((name, p.knights[name]))
                blue_team = []
                for p in self.blue_team.values():
                    name = list(p.knights.keys())[0]
                    blue_team.append((name, p.knights[name]))

            engine = Engine(score=self.score,
                            red_team=red_team,
                            blue_team=blue_team,
                            speedup=speedup,
                            show_messages=show_messages)
            winner = engine.run(safe=safe)
            self.update_scores(winner)

            score = self.score
            a_team_has_won = False
            for team in ('red', 'blue'):
                if score[team] == self.first_to:
                    self.update_winner(team)
                    a_team_has_won = True
            if self.manager is not None:
                self.manager.save()
            if a_team_has_won:
                return

            input(f"Current score: red={score['red']} "
                  f"blue={score['blue']}. Start next round")

        score = self.score
        if score['red'] > score['blue']:
            self.update_winner('red')
        if score['blue'] > score['red']:
            self.update_winner('blue')


class JupyterMatch(Match):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)