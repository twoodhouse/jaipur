from enum import Enum

class Action(Enum):
    TakeCard, TradeCards, TakeCamels, PlayCards = range(4)

class Resource(Enum):
    Leather, Cloth, Spice, Silver, Gold, Gem, Camel = range(7)

class Chip():
    def __init__(self, value, resource = None, hidden = False):
        self.value = value
        self.resource = resource
