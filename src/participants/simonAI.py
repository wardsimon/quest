from madsAI import MadsWarrior


class SimonWarrior(MadsWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'Simon'


team = {
    'Anakin': SimonWarrior,
    'ObiOne': SimonWarrior,
    'Darth-Vader': SimonWarrior
}
