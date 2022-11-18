from game_map import Map
from knight import Knight
from fight import fight
from engine import Engine

from neil import team as NeilTeam
from mads import team as MadsTeam

if __name__ == '__main__':

    best_of = 5
    first_to = 3

    match_score = {'red': 0, 'blue': 0, 'count': 0}
    for n in range(best_of):
        match_score['count'] += 1
        engine = Engine(score=match_score,
                        red_team=NeilTeam,
                        blue_team=MadsTeam)
        winner = engine.run()
        if winner is not None:
            match_score[winner] += 1
        for team in match_score:
            if match_score[team] == first_to:
                break
        input('start next match')
