from madsAI import MadsWarrior


class DrewWarrior(MadsWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'Drew'


team = {'Anakin': DrewWarrior, 'ObiOne': DrewWarrior, 'Caspar': DrewWarrior}
