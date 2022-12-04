from madsAI import MadsWarrior


class AfonsoWarrior(MadsWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'Afonso'


team = {
    'AFOne': AfonsoWarrior,
    'AFTwo': AfonsoWarrior,
    'AFThree': AfonsoWarrior
}
