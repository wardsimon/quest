from engine import Engine


class Match:

    def __init__(self,
                 red_team,
                 blue_team,
                 number,
                 phase,
                 rounds,
                 manager=None):
        self.red_team = red_team
        self.blue_team = blue_team
        self.number = number
        self.rounds = [] if rounds is None else rounds
        self.phase = phase
        self.manager = manager
        self.best_of = 5
        self.first_to = self.best_of // 2 + 1
        self.match_winner = None

    def to_dict(self):
        return {
            'phase': self.phase,
            'red': list(self.red_team.keys()),
            'blue': list(self.blue_team.keys()),
            'rounds': self.rounds,
            'number': self.number,
            'winner': self.match_winner
        }

    def update_scores(self, winner):
        self.rounds.append(winner)
        if winner == 'red':
            for p in self.red_team.values():
                p.rounds_won += 1
        elif winner == 'blue':
            for p in self.blue_team.values():
                p.rounds_won += 1

    @property
    def score(self):
        s = {'red': 0, 'blue': 0, 'count': len(self.rounds) + 1}
        for r in self.rounds:
            if r is not None:
                s[r] += 1
        return s

    def is_complete(self):
        return not (len(self.rounds) < self.best_of)

    def update_winner(self, winning_team):
        self.match_winner = winning_team

    def play(self, speedup=1.0, show_messages=False):
        # best_of = 5
        # first_to = 3

        # match_score = {
        #     'red': starting_score['red'],
        #     'blue': starting_score['blue'],
        #     'count': 0
        # }

        for n in range(len(self.rounds), self.best_of):
            # match_score['count'] = n + 1

            if self.phase == 1:
                red = list(self.red_team.keys())[0]
                blue = list(self.blue_team.keys())[0]
                # red_team = (red, [(k, v)
                #                   for k, v in match.red_team[red].knights.items()])
                # blue_team = (blue, [
                #     (k, v) for k, v in match.blue_team[blue].knights.items()
                # ])
                red_team = [(k, v)
                            for k, v in self.red_team[red].knights.items()]
                blue_team = [(k, v)
                             for k, v in self.blue_team[blue].knights.items()]

            engine = Engine(score=self.score,
                            red_team=red_team,
                            blue_team=blue_team,
                            speedup=speedup,
                            show_messages=show_messages)
            winner = engine.run()
            self.update_scores(winner)
            self.manager.save()

            # if winner is not None:
            #     match_score[winner] += 1
            # # Write score to file
            # with open('score.txt', 'a') as f:
            #     f.write(
            #         f"|Round:{match_score['count']}:{red_team[0]}:"
            #         f"{match_score['red']}:{blue_team[0]}:{match_score['blue']}")
            # for team in ('red', 'blue'):
            #     if match_score[team] == first_to:
            #         return
            score = self.score
            for team in score:
                if score[team] == self.first_to:
                    self.update_winner(team)
                    return
            input(f"Current score: red={score['red']} "
                  f"blue={score['blue']}. Start next round")

        score = self.score
        if score['red'] > score['blue']:
            self.update_winner('red')
        if score['blue'] > score['red']:
            self.update_winner('blue')
