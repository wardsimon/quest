from pathlib import Path
from itertools import combinations
import numpy as np
from random import shuffle
import yaml


class Participant:

    def __init__(self, name, knights, rounds_won=0, matches_won=0):
        self.name = name
        self.knights = knights
        self.rounds_won = rounds_won
        self.matches_won = matches_won

    def to_dict(self):
        return {'rounds_won': self.rounds_won, 'matches_won': self.matches_won}


class Match:

    def __init__(self, red_team, blue_team, number, phase):
        self.red_team = red_team
        self.blue_team = blue_team
        self.number = number
        self.rounds = []
        self.phase = phase

    def to_dict(self):
        return {
            'phase': self.phase,
            'red': list(self.red_team.keys()),
            'blue': list(self.blue_team.keys()),
            'rounds': self.rounds
        }


# with open('UserDetails.yaml', 'w') as f:
#     data = yaml.dump(user_details, f, sort_keys=False, default_flow_style=False)


class Manager:

    def __init__(self, *participants):

        self.participants = {}
        for team in participants:
            creator = list(team.values())[0]().creator
            self.participants[creator] = Participant(name=creator,
                                                     knights=team)

        self.matches = []
        self.phase = 0

        file = Path("tournament.xml")
        if file.exists():
            self.load()
        else:
            self.make_tournament()

    def make_tournament(self):
        matches = list(combinations(self.participants.keys(), 2))
        shuffle(matches)
        for i, match in enumerate(matches):
            red = match[0]
            blue = match[1]
            self.matches.append(
                Match(red_team={red: self.participants[red]},
                      blue_team={blue: self.participants[blue]},
                      number=i + 1,
                      phase=1))

    def save(self):
        out = {
            'participants':
            {name: p.to_dict()
             for name, p in self.participants.items()},
            'matches': {m.number: m.to_dict()
                        for m in self.matches}
        }
        with open('UserDetails.yaml', 'w') as f:
            yaml.dump(out, f, sort_keys=False, default_flow_style=False)


def other():
    first_phase = [[[match[0]] * 3, [match[1]] * 3] for match in matches]
    with open(match_list_file, 'w') as f:
        f.write('First phase\n')
        for match in first_phase:
            f.write(':'.join(match[0]) + ':' + ':'.join(match[1]) + '\n')
    #         # f.write(f'{match[0]}:{match[1]}\n')

    n_per_round = 6
    matches_per_participant = len(participants) - 1

    l = list(participants.keys()) * matches_per_participant
    sets = []
    second_phase = []
    while len(l) > 0:
        possibles = list(set(l))
        this_round = []
        # print('possibles', possibles)
        if len(possibles) < n_per_round:
            div = len(possibles) // 2
            red = possibles[:div]
            blue = possibles[div:]
            l.clear()
        else:
            for i in range(n_per_round):
                ind = np.random.choice(range(len(possibles)))
                this_round.append(possibles.pop(ind))
            red = set(this_round[:3])
            blue = set(this_round[3:])
        if (red not in sets) and (blue not in sets):
            second_phase.append([list(red), list(blue)])
            sets += [red, blue]
            for name in this_round:
                l.remove(name)

    match_list_file = Path("match_list.txt")
    if match_list_file.exists():
        with open(match_list_file, 'r') as f:
            matches = f.readlines()
        n = 0
        count = True
        match_list = []
        for match in matches:
            if ':' in match:
                li = match.strip().split(':')
                match_list.append([li[:3], li[3:]])
                if count:
                    n += 1
            if 'Second phase' in match:
                count = False
        return match_list, n
    else:
        matches = list(combinations(participants.keys(), 2))
        shuffle(matches)
        first_phase = [[[match[0]] * 3, [match[1]] * 3] for match in matches]
        with open(match_list_file, 'w') as f:
            f.write('First phase\n')
            for match in first_phase:
                f.write(':'.join(match[0]) + ':' + ':'.join(match[1]) + '\n')
        #         # f.write(f'{match[0]}:{match[1]}\n')

        n_per_round = 6
        matches_per_participant = len(participants) - 1

        l = list(participants.keys()) * matches_per_participant
        sets = []
        second_phase = []
        while len(l) > 0:
            possibles = list(set(l))
            this_round = []
            # print('possibles', possibles)
            if len(possibles) < n_per_round:
                div = len(possibles) // 2
                red = possibles[:div]
                blue = possibles[div:]
                l.clear()
            else:
                for i in range(n_per_round):
                    ind = np.random.choice(range(len(possibles)))
                    this_round.append(possibles.pop(ind))
                red = set(this_round[:3])
                blue = set(this_round[3:])
            if (red not in sets) and (blue not in sets):
                second_phase.append([list(red), list(blue)])
                sets += [red, blue]
                for name in this_round:
                    l.remove(name)
        with open(match_list_file, 'a') as f:
            f.write('Second phase\n')
            for match in second_phase:
                f.write(
                    ':'.join([item for sublist in match
                              for item in sublist]) + '\n')

        return first_phase + second_phase, len(first_phase)

        tree = ET.parse('score.xml')
        root = tree.getroot()

        print()