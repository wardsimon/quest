from neilAI import NeilWarrior


class GregWarrior(NeilWarrior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = 'Greg'


team = {'Arthur': GregWarrior, 'GGGG': GregWarrior, 'Lancelot': GregWarrior}
