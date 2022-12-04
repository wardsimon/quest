from madsAI import MadsWarrior


class TonyWarrior(MadsWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'Tony'


team = {'TonyA': TonyWarrior, 'TonyB': TonyWarrior, 'TonyC': TonyWarrior}
