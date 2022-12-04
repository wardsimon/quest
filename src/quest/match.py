from engine import Engine


class Match:

    def __init__(self,
                 red_team,
                 blue_team,
                 number,
                 phase,
                 rounds=None,
                 manager=None,
                 winner=None):
        self.red_team = red_team
        self.blue_team = blue_team
        self.number = number
        # self.rounds = ['red', 'red', None, 'red']
        # print(self.score)
        self.rounds = [] if rounds is None else rounds
        self.phase = phase
        self.manager = manager
        self.best_of = 5
        self.first_to = self.best_of // 2 + 1
        self.match_winner = winner
        # print(self.first_to)
        # input('ll')

    def to_dict(self):
        return {
            'phase': self.phase,
            'red': list(self.red_team.keys()),
            'blue': list(self.blue_team.keys()),
            'rounds': self.rounds,
            'number': self.number,
            'winner': self.match_winner
        }

    def to_string(self):
        return (f'red={list(self.red_team.keys())} VS '
                f'blue={list(self.blue_team.keys())}')

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
        return (self.match_winner
                is not None) or (not (len(self.rounds) < self.best_of))

    def update_winner(self, winning_team):
        self.match_winner = winning_team
        if winning_team == 'red':
            for p in self.red_team.values():
                p.matches_won += 1
        elif winning_team == 'blue':
            for p in self.blue_team.values():
                p.matches_won += 1

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
            print(score)
            a_team_has_won = False
            for team in ('red', 'blue'):
                # print(team, score[team], self.first_to,
                #       score[team] == self.first_to)
                if score[team] == self.first_to:
                    self.update_winner(team)
                    # print('RETURNING')
                    a_team_has_won = True
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
