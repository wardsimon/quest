import sys

sys.path.append('../participants')

from manager import Manager

from neilAI import team as NeilTeam
from madsAI import team as MadsTeam
from gregAI import team as GregTeam
from drewAI import team as DrewTeam
from simonAI import team as SimonTeam
from janAI import team as JanTeam
from afonsoAI import team as AfonsoTeam
from tonyAI import team as TonyTeam

if __name__ == '__main__':

    manager = Manager(NeilTeam, MadsTeam, GregTeam, DrewTeam, SimonTeam,
                      JanTeam, AfonsoTeam, TonyTeam)

    while ((match := manager.next_match()) is not None):
        input(f'Next match is: {match.to_string()}')
        match.play(speedup=1, show_messages=False)
        manager.show_scores()

    manager.show_scores()
    input('End of tournament!')
