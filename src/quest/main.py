from pathlib import Path
from itertools import combinations
import numpy as np
from random import shuffle
import turtle
# from engine import Engine
from manager import Manager

from neilAI import team as NeilTeam
from madsAI import team as MadsTeam
from gregAI import team as GregTeam
from drewAI import team as DrewTeam
from simonAI import team as SimonTeam
from janAI import team as JanTeam
from afonsoAI import team as AfonsoTeam
from tonyAI import team as TonyTeam

# def generate_match_list(participants):
#     match_list_file = Path("match_list.txt")
#     if match_list_file.exists():
#         with open(match_list_file, 'r') as f:
#             matches = f.readlines()
#         n = 0
#         count = True
#         match_list = []
#         for match in matches:
#             if ':' in match:
#                 li = match.strip().split(':')
#                 match_list.append([li[:3], li[3:]])
#                 if count:
#                     n += 1
#             if 'Second phase' in match:
#                 count = False
#         return match_list, n
#     else:
#         matches = list(combinations(participants.keys(), 2))
#         shuffle(matches)
#         first_phase = [[[match[0]] * 3, [match[1]] * 3] for match in matches]
#         with open(match_list_file, 'w') as f:
#             f.write('First phase\n')
#             for match in first_phase:
#                 f.write(':'.join(match[0]) + ':' + ':'.join(match[1]) + '\n')
#         #         # f.write(f'{match[0]}:{match[1]}\n')

#         n_per_round = 6
#         matches_per_participant = len(participants) - 1

#         l = list(participants.keys()) * matches_per_participant
#         sets = []
#         second_phase = []
#         while len(l) > 0:
#             possibles = list(set(l))
#             this_round = []
#             # print('possibles', possibles)
#             if len(possibles) < n_per_round:
#                 div = len(possibles) // 2
#                 red = possibles[:div]
#                 blue = possibles[div:]
#                 l.clear()
#             else:
#                 for i in range(n_per_round):
#                     ind = np.random.choice(range(len(possibles)))
#                     this_round.append(possibles.pop(ind))
#                 red = set(this_round[:3])
#                 blue = set(this_round[3:])
#             if (red not in sets) and (blue not in sets):
#                 second_phase.append([list(red), list(blue)])
#                 sets += [red, blue]
#                 for name in this_round:
#                     l.remove(name)
#         with open(match_list_file, 'a') as f:
#             f.write('Second phase\n')
#             for match in second_phase:
#                 f.write(
#                     ':'.join([item for sublist in match
#                               for item in sublist]) + '\n')

#         return first_phase + second_phase, len(first_phase)

# def starting_match_index_and_score(match_list):
#     # Read score file if present
#     score_file = Path("score.txt")
#     if score_file.exists():
#         with open(score_file, 'r') as f:
#             scores = f.readlines()
#         last_score = scores[-1].split('|')[-1].split(':')
#         ind = len(scores)
#         if not scores[-1].strip().endswith('END'):
#             ind -= 1
#         return ind, int(last_score[1]) - 1, {
#             'red': int(last_score[3]),
#             'blue': int(last_score[5])
#         }
#     else:
#         return 0, -1, {'red': 0, 'blue': 0}


def show_scores(next_match=None):
    with open('score.txt', 'r') as f:
        scores = f.readlines()
    participants = {}
    for line in scores:
        final_score = line.split('|')[-1].split(':')
        red_team = final_score[2]
        red_score = final_score[3]
        blue_team = final_score[4]
        blue_score = final_score[5]
        red_victory = int(red_score > blue_score)
        blue_victory = int(blue_score > red_score)
        if red_team not in participants:
            participants[red_team] = {
                'rounds': red_score,
                'matches': red_victory
            }
        else:
            participants[red_team]['rounds'] += red_score
            participants[red_team]['matches'] += red_victory
        if blue_team not in participants:
            participants[blue_team] = {
                'rounds': blue_score,
                'matches': blue_victory
            }
        else:
            participants[blue_team]['rounds'] += blue_score
            participants[blue_team]['matches'] += blue_victory

    text = '======= SCORES =======\n'
    for k, v in sorted(participants.items(),
                       key=lambda item:
                       (item[1]['rounds'], item[1]['matches']),
                       reverse=True):
        string = f"{k}: rounds won={v['rounds']}, matches won={v['matches']}"
        text += string + '\n'
    print(text)
    if next_match is not None:
        text += next_match + '\n'
    screen = turtle.Screen()
    screen.clearscreen()
    screen.tracer(0)
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    pen.penup()
    pen.goto(500, 800)
    pen.pendown()
    pen.write(text, move=False, align="left", font=('Arial', 18, 'normal'))
    pen.penup()


def end_match(next_match=None):
    with open('score.txt', 'a') as f:
        f.write(':END\n')
    show_scores(next_match=next_match)


# def start_match(red_team,
#                 blue_team,
#                 round_number=-1,
#                 starting_score={
#                     'red': 0,
#                     'blue': 0
#                 },
#                 speedup=1.0,
#                 show_messages=False):
# def play_match(match, speedup=1.0, show_messages=False):

#     best_of = 5
#     first_to = 3

#     # match_score = {
#     #     'red': starting_score['red'],
#     #     'blue': starting_score['blue'],
#     #     'count': 0
#     # }

#     for n in range(len(match.rounds), best_of):
#         # match_score['count'] = n + 1

#         if match.phase == 1:
#             red = list(match.red_team.keys())[0]
#             blue = list(match.blue_team.keys())[0]
#             # red_team = (red, [(k, v)
#             #                   for k, v in match.red_team[red].knights.items()])
#             # blue_team = (blue, [
#             #     (k, v) for k, v in match.blue_team[blue].knights.items()
#             # ])
#             red_team = [(k, v) for k, v in match.red_team[red].knights.items()]
#             blue_team = [(k, v)
#                          for k, v in match.blue_team[blue].knights.items()]

#         engine = Engine(score=match.score,
#                         red_team=red_team,
#                         blue_team=blue_team,
#                         speedup=speedup,
#                         show_messages=show_messages)
#         winner = engine.run()
#         match.update_scores(winner)
#         match.manager.save()

#         # if winner is not None:
#         #     match_score[winner] += 1
#         # # Write score to file
#         # with open('score.txt', 'a') as f:
#         #     f.write(
#         #         f"|Round:{match_score['count']}:{red_team[0]}:"
#         #         f"{match_score['red']}:{blue_team[0]}:{match_score['blue']}")
#         # for team in ('red', 'blue'):
#         #     if match_score[team] == first_to:
#         #         return
#         score = match.score
#         if max(score.values()) == first_to:
#             return
#         input(f"Current score: red={score['red']} "
#               f"blue={score['blue']}. Start next round")

if __name__ == '__main__':

    # teams = [
    #     NeilTeam, MadsTeam, GregTeam, DrewTeam, SimonTeam, JanTeam, AfonsoTeam,
    #     TonyTeam
    # ]

    manager = Manager(NeilTeam, MadsTeam, GregTeam, DrewTeam, SimonTeam,
                      JanTeam, AfonsoTeam, TonyTeam)
    print([m.to_dict() for m in manager.matches])
    # manager.save()

    while ((match := manager.next_match()) is not None):
        # print(match.to_dict())
        input(f'Next match is: {match.to_string()}')
        match.play(speedup=1.0, show_messages=False)
        manager.show_scores()
        # next_match = None
        # if i < len(match_list) - 1:
        #     next_match = (f'Next match is: red={match_list[i+1][0]} '
        #                   f'VS blue={match_list[i+1][1]}')
        # end_match(next_match=next_match)
        # round_number = 0

    show_scores()
    input('End of tournament!')

    exit()

    # participants = {}
    # for team in teams:
    #     creator = list(team.values())[0]().creator
    #     participants[creator] = team

    # match_list, first_phase_len = generate_match_list(participants)
    # # print(match_list)
    # # print('==================')
    # # exit()
    # match_index, round_number, score = starting_match_index_and_score(
    #     match_list)
    # # print('match_index')
    # # print(match_index)
    # # print('round_number')
    # # print(round_number)
    # # print('score')
    # # print(score)
    # # exit()
    # # match_index = 28
    # for i in range(match_index, len(match_list)):
    #     if i < first_phase_len:
    #         # print('match_list[i]', match_list[i])
    #         red = match_list[i][0][0]
    #         blue = match_list[i][1][0]
    #         red_team = (red, [(k, v) for k, v in participants[red].items()])
    #         blue_team = (blue, [(k, v) for k, v in participants[blue].items()])
    #     else:
    #         # print(match_list[i][:3])
    #         red = '+'.join(match_list[i][0])
    #         blue = '+'.join(match_list[i][1])
    #         red_knights = []
    #         # print(match_list[i])
    #         for author in match_list[i][0]:
    #             d = participants[author]
    #             key = list(d.keys())[0]
    #             red_knights.append((key, d[key]))
    #         red_team = (red, red_knights)
    #         blue_knights = []
    #         for author in match_list[i][1]:
    #             d = participants[author]
    #             key = list(d.keys())[0]
    #             blue_knights.append((key, d[key]))
    #         blue_team = (blue, blue_knights)
    #     # print(red_team)
    #     # print(blue_team)
    #     input(f'Next match is: red={red} VS blue={blue}')
    #     start_match(red_team=red_team,
    #                 blue_team=blue_team,
    #                 round_number=round_number,
    #                 starting_score=score,
    #                 speedup=1.0,
    #                 show_messages=False)
    #     next_match = None
    #     if i < len(match_list) - 1:
    #         next_match = (f'Next match is: red={match_list[i+1][0]} '
    #                       f'VS blue={match_list[i+1][1]}')
    #     end_match(next_match=next_match)
    #     round_number = 0

    # show_scores()
    # input('End of tournament!')

    # # # Second phase:
    # # participants = [
    # #     'Neil', 'Mads', 'Drew', 'Greg', 'JanLukas', 'Simon', 'Afonso'
    # # ]

    # # n_per_round = 6
    # # matches_per_participant = 4

    # # l = participants * matches_per_participant

    # # sets = []
    # # match_list = []

    # # while len(l) > 0:
    # #     possibles = list(set(l))
    # #     this_round = []
    # #     print('possibles', possibles)
    # #     if len(possibles) < n_per_round:
    # #         div = len(possibles) // 2
    # #         red = possibles[:div]
    # #         blue = possibles[div:]
    # #         l.clear()
    # #     else:
    # #         for i in range(n_per_round):
    # #             ind = np.random.choice(range(len(possibles)))
    # #             this_round.append(possibles.pop(ind))
    # #         red = set(this_round[:3])
    # #         blue = set(this_round[3:])
    # #     if (red not in sets) and (blue not in sets):
    # #         match_list.append([red, blue])
    # #         sets += [red, blue]
    # #         for name in this_round:
    # #             l.remove(name)
    # #     print("sets", sets)
    # #     print('match_list', match_list)
    # #     print('list', l)
    # #     print('============')
