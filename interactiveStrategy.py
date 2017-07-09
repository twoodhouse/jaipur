from util import Resource, Action

class InteractiveStrategy():
    def __init__(self):
        pass
    def actionChoice(self, gameView):
        print(gameView)
        response = input('Action >> ')
        return Action[response]
    def takeCardChoice(self, gameView):
        response = input('Card Choice >> ')
        return Resource[response]
    def tradeCardsChoice(self, gameView):
        numCards = int(input('Number of Resources to trade >> '))
        outR = []
        inR = []
        for i in range(numCards):
            outR.append(Resource[input('Resource to trade out >> ')])
        for i in range(numCards):
            inR.append(Resource[input('Resource to get from center >> ')])
        return (outR, inR)
    def playCardsChoice(self, gameView):
        numCards = int(input('Number of Resources to play >> '))
        resourcesToPlay = []
        for i in range(numCards):
            resourcesToPlay.append(Resource[input('Resource to play >> ')])
        return resourcesToPlay
