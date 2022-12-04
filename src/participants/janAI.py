from madsAI import MadsWarrior


class JanWarrior(MadsWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'JanLukas'


team = {'One': JanWarrior, 'Two': JanWarrior, 'Three': JanWarrior}
