from abc import abstractmethod


class BaseAI:

    def __init__(self, creator=None):
        self.heading = 0
        self.goto = None
        self.creator = creator

    @abstractmethod
    def run(self, t, info):
        return
