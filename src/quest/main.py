import os
import sys
from pathlib import Path
from itertools import combinations
from random import shuffle

from game_map import Map
from knight import Knight
from fight import fight
from engine import Engine

from neilAI import team as NeilTeam
from mads import team as MadsTeam


def generate_match_list(participants):
    match_list_file = Path("match_list.txt")
    if match_list_file.exists():
        with open(match_list_file, 'r') as f:
            match_list = f.readlines()
        return [match.strip().split(':') for match in match_list]
    else:
        match_list = list(combinations(participants.keys(), 2))
        shuffle(match_list)
        with open(match_list_file, 'w') as f:
            for match in match_list:
                f.write(f'{match[0]}:{match[1]}\n')
        return match_list


def starting_match_index_and_score(match_list):
    # Read score file if present
    score_file = Path("score.txt")
    if score_file.exists():
        with open(score_file, 'r') as f:
            scores = f.readlines()
        last_score = scores[-1].split('|')[-1].split(':')
        # round_number = last_score[1]
        ind = len(scores)
        if not scores[-1].strip().endswith('END'):
            ind -= 1
        return ind, int(last_score[1]) - 1, {
            'red': int(last_score[3]),
            'blue': int(last_score[5])
        }
    else:
        return 0, -1, {'red': 0, 'blue': 0}


def end_match():
    with open('score.txt', 'a') as f:
        f.write(':END\n')


def start_match(red_team, blue_team, round_number, starting_score, speedup):
    best_of = 5
    first_to = 3

    match_score = {
        'red': starting_score['red'],
        'blue': starting_score['blue'],
        'count': 0
    }
    # print(round_number, match_score)
    for n in range(round_number + 1, best_of):
        # match_score['count'] += 1
        match_score['count'] = n + 1
        engine = Engine(score=match_score,
                        red_team=red_team[1],
                        blue_team=blue_team[1],
                        speedup=speedup)
        winner = engine.run()
        if winner is not None:
            match_score[winner] += 1
        # Write score to file
        with open('score.txt', 'a') as f:
            f.write(
                f"|Round:{match_score['count']}:{red_team[0]}:{match_score['red']}:{blue_team[0]}:{match_score['blue']}"
            )
        for team in ('red', 'blue'):
            if match_score[team] == first_to:
                # end_match()
                # print('score first_to was reached', team, match_score[team])
                return
        input('start next round')
    # end_match()
    # with open('score.txt', 'a') as f:
    #     f.write(':END\n')
    # print('end of rounds', n, round_number, round_number + 1, best_of)


if __name__ == '__main__':
    participants = {
        'Neil': NeilTeam,
        'Mads': MadsTeam,
        # 'Greg': NeilTeam,
        # 'Drew': MadsTeam
    }
    match_list = generate_match_list(participants)
    # print(match_list)
    match_index, round_number, score = starting_match_index_and_score(
        match_list)
    # print('starting index', match_index, round_number, score)
    for i in range(match_index, len(match_list)):
        red = match_list[i][0]
        blue = match_list[i][1]
        # print(red, blue)
        start_match(red_team=(red, participants[red]),
                    blue_team=(blue, participants[blue]),
                    round_number=round_number,
                    starting_score=score,
                    speedup=1.0)
        end_match()
