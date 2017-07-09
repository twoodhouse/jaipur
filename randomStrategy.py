from util import Resource, Action
import random

class RandomStrategy():
    def __init__(self):
        pass
    def actionChoice(self, gameView):
        takeCardRelativeWeight = 0
        playCardsRelativeWeight = 0
        takeCamelsRelativeWeight = 0
        tradeCardsRelativeWeight = 0
        if len(gameView.myHand) < 7 and containsNonCamelResource(gameView.center):
            takeCardRelativeWeight = 5
        if containsCamelResource(gameView.center):
            takeCamelsRelativeWeight = 5
        if handHasPlayableSet(gameView.myHand):
            playCardsRelativeWeight = 5
        if tradePossible(gameView.myHand, gameView.myCamels, gameView.center):
            tradeCardsRelativeWeight = 0
        return weighted_choice([(Action.PlayCards, playCardsRelativeWeight),
            (Action.TakeCamels, takeCamelsRelativeWeight),
            (Action.TakeCard, takeCardRelativeWeight),
            (Action.TradeCards, tradeCardsRelativeWeight)])
    def takeCardChoice(self, gameView):
        options = set(gameView.center)
        if Resource.Camel in options:
            options.remove(Resource.Camel)
        return random.choice(tuple(options))
    def tradeCardsChoice(self, gameView):
        return None
    def playCardsChoice(self, gameView):
        cardToPlay = most_common(gameView.myHand)
        cards = []
        for card in gameView.myHand:
            if card == cardToPlay:
                cards.append(card)
        if cardToPlay == Resource.Gold or cardToPlay == Resource.Gem or cardToPlay == Resource.Silver:
            if len(cards) < 2:
                if Resource.Leather in gameView.myHand:
                    cards = [Resource.Leather]
                elif Resource.Cloth in gameView.myHand:
                    cards = [Resource.Cloth]
                elif Resource.Spice in gameView.myHand:
                    cards = [Resource.Spice]
        return cards

def containsNonCamelResource(lst):
    for e in lst:
        if e != Resource.Camel:
            return True
    return False

def containsCamelResource(lst):
    for e in lst:
        if e == Resource.Camel:
            return True
    return False

def handHasPlayableSet(hand):
    for e in hand:
        if e == Resource.Leather or e == Resource.Cloth or e == Resource.Spice:
            return True
    #check for diamond, gold, or silver set
    gemCount = 0
    goldCount = 0
    silverCount = 0
    for e in hand:
        if e == Resource.Gem:
            gemCount += 1
        if e == Resource.Gold:
            goldCount += 1
        if e == Resource.Silver:
            silverCount += 1
    if gemCount >= 2 or goldCount >= 2 or silverCount >= 2:
        return True
    return False

def tradePossible(hand, camels, center):
    if len(hand) + len(camels) < 2:
        return False
    if len(camels) >= 2:
        return True
    handSet = set(hand)
    if len(handSet) >= 3:
        return True
    centerSet = set(center)
    if len(centerSet) >=3:
        return True
    return False #note - there are more circumstances where it is always possible to trade, but I don't feel like writing the code for it.

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w

def most_common(lst):
  return max(set(lst), key=lst.count)
