from util import Action, Resource, Chip
from random import shuffle
from copy import deepcopy

def runJaipur(strategies):
    p1Strategy, p2Strategy = strategies
    #Set up table (mainDeck, center, p1Hand, p2Hand)
    mainDeck = ([Resource.Leather] * 10 +
        [Resource.Cloth] * 8 +
        [Resource.Spice] * 8 +
        [Resource.Silver] * 6 +
        [Resource.Gold] * 6 +
        [Resource.Gem] * 6 +
        [Resource.Camel] * 8)
    shuffle(mainDeck)
    center = [Resource.Camel] * 3
    center.append(mainDeck.pop())
    center.append(mainDeck.pop())
    p1Hand = []
    p2Hand = []
    p1Camels = []
    p2Camels = []
    for i in range(5):
        p1Hand.append(mainDeck.pop())
        p2Hand.append(mainDeck.pop())
    for resource in p1Hand:
        if resource == Resource.Camel:
            p1Camels.append(resource)
        p1Hand = list(filter((Resource.Camel).__ne__, p1Hand))
    for resource in p2Hand:
        if resource == Resource.Camel:
            p2Camels.append(resource)
        p2Hand = list(filter((Resource.Camel).__ne__, p2Hand))
    #Set up chip stacks (chipStacks)
    chipStacks = {}
    chipStacks[Resource.Leather] = ([Chip(1), Chip(1), Chip(1), Chip(1), Chip(1), Chip(1), Chip(2), Chip(3), Chip(4)])
    chipStacks[Resource.Spice] = ([Chip(1), Chip(1), Chip(2), Chip(2), Chip(3), Chip(3), Chip(5)])
    chipStacks[Resource.Cloth] = ([Chip(1), Chip(1), Chip(2), Chip(2), Chip(3), Chip(3), Chip(5)])
    chipStacks[Resource.Silver] = ([Chip(5), Chip(5), Chip(5), Chip(5), Chip(5)])
    chipStacks[Resource.Gold] = ([Chip(5), Chip(5), Chip(5), Chip(6), Chip(6)])
    chipStacks[Resource.Gem] = ([Chip(5), Chip(5), Chip(5), Chip(7), Chip(7)])
    chipStacks[3] = ([Chip(1), Chip(1), Chip(2), Chip(2), Chip(2), Chip(3), Chip(3)])
    chipStacks[4] = ([Chip(4), Chip(4), Chip(5), Chip(5), Chip(6), Chip(6)])
    chipStacks[5] = ([Chip(8), Chip(8), Chip(9), Chip(10), Chip(10)])
    shuffle(chipStacks[3])
    shuffle(chipStacks[4])
    shuffle(chipStacks[5])
    #Initialize player chip stacks
    p1ChipStacks = {Resource.Leather: [], Resource.Spice: [], Resource.Cloth: [], Resource.Silver: [], Resource.Gold: [], Resource.Gem: [], 3: [], 4: [], 5: []}
    p2ChipStacks = {Resource.Leather: [], Resource.Spice: [], Resource.Cloth: [], Resource.Silver: [], Resource.Gold: [], Resource.Gem: [], 3: [], 4: [], 5: []}

    #Start Game
    winner = None
    description = ''
    firstPlayerTurn = True
    priorAction = None
    priorActionDetails = None
    actionDetails = None
    while not winner:
        gameOver = False
        if firstPlayerTurn:
            strategy = p1Strategy
            hand = p1Hand
            opponentHand = p2Hand
            camels = p1Camels
            opponentCamels = p2Camels
            playerName = 'P1'
            opponentName = 'P2'
            playerChipStacks = p1ChipStacks
            opponentChipStacks = p2ChipStacks
        else:
            strategy = p2Strategy
            hand = p2Hand
            opponentHand = p1Hand
            camels = p2Camels
            opponentCamels = p1Camels
            playerName = 'P2'
            opponentName = 'P1'
            playerChipStacks = p2ChipStacks
            opponentChipStacks = p1ChipStacks
        gv = GameView(center, chipStacks, len(mainDeck), playerName, hand, camels, playerChipStacks, len(opponentHand), len(opponentCamels), opponentChipStacks, priorAction, priorActionDetails)
        action = strategy.actionChoice(gv)
        if type(action) != Action:
            winner = opponentName
            description = '{} disqulified for not giving a valid action'.format(playerName)
        #ACTION RULES
        if action == Action.PlayCards:
            cardsToPlay = strategy.playCardsChoice(gv)
            actionDetails = cardsToPlay
            if not checkEqual(cardsToPlay):
                winner = opponentName
                description = '{} disqulified for trying to play a set of unlike cards for chips'.format(playerName)
            if cardsToPlay[0] == Resource.Camel:
                winner = opponentName
                description = '{} disqulified for trying to play camels for chips'.format(playerName)
            for card in cardsToPlay:
                if card in hand:
                    hand.remove(card)
                else:
                    winner = opponentName
                    description = '{} disqulified for trying to play a card he did not have'.format(playerName)
            chips = []
            for i in range(len(cardsToPlay)):
                if len(chipStacks[cardsToPlay[0]]) >= 1:
                    chips.append(chipStacks[cardsToPlay[0]].pop())
            playerChipStacks[cardsToPlay[0]].extend(chips)
            if len(cardsToPlay) < 2 and (cardsToPlay[0] == Resource.Gem or cardsToPlay[0] == Resource.Silver or cardsToPlay[0] == Resource.Gold):
                winner = opponentName
                description = '{} disqulified for playing less than 2 cards with a Gem or Gold or Siver set'.format(playerName)
            if len(cardsToPlay) > 2:
                if len(chipStacks[len(cardsToPlay)]) >= 1:
                    playerChipStacks[len(cardsToPlay)].append(chipStacks[len(cardsToPlay)].pop())
        elif action == Action.TakeCamels:
            camelsTaken = 0
            for card in center:
                if card == Resource.Camel:
                    camelsTaken += 1
                    camels.append(card)
            center = list(filter((Resource.Camel).__ne__, center))
            for i in range(camelsTaken):
                if len(mainDeck) > 0:
                    center.append(mainDeck.pop())
                else:
                    gameOver = True
            if camelsTaken == 0:
                winner = opponentName
                description = '{} disqulified for trying to take all camels when there are none available'.format(playerName)
        elif action == Action.TakeCard:
            cardToTake = strategy.takeCardChoice(gv)
            actionDetails = cardToTake
            if cardToTake == Resource.Camel:
                winner = opponentName
                description = '{} disqulified for taking a camel card from the center (can only take resources)'.format(playerName)
            if len(hand) >= 7:
                winner = opponentName
                description = '{} disqulified for taking a card when he already has 7 cards'.format(playerName)
            if cardToTake in center:
                center.remove(cardToTake)
                hand.append(cardToTake)
                if len(mainDeck) > 0:
                    center.append(mainDeck.pop())
                else:
                    gameOver = True
            else:
                winner = opponentName
                description = '{} disqulified for trying to take a card from the center that doesn\'t exist'.format(playerName)
        elif action == Action.TradeCards:
            cardsToTrade = strategy.tradeCardsChoice(gv)
            actionDetails = cardsToTrade
            for cardi in cardsToTrade[0]:
                for cardj in cardsToTrade[1]:
                    if cardi == cardj:
                        winner = opponentName
                        description = '{} disqulified for trying to trade out and in the same resource'.format(playerName)
            if len(cardsToTrade[0]) < 2:
                winner = opponentName
                description = '{} disqulified for trying to trade out less than two cards'.format(playerName)
            for cardOut in cardsToTrade[0]:
                if cardOut == Resource.Camel:
                    camels.pop()
                else:
                    if cardOut in hand:
                        hand.remove(cardOut)
                    else:
                        winner = opponentName
                        description = '{} disqulified for trying to trade out a card he did not have'.format(playerName)
                center.append(cardOut)
            for cardIn in cardsToTrade[1]:
                if cardIn in center:
                    center.remove(cardIn)
                else:
                    winner = opponentName
                    description = '{} disqulified for trying to take a card in a trade that is not in the center'.format(playerName)
                if cardIn == Resource.Camel:
                    camels.append(cardIn)
                else:
                    hand.append(cardIn)
            if len(hand) > 7:
                winner = opponentName
                description = '{} disqulified for trading so that there are now more than 7 cards in his hand'.format(playerName)
        stacksDone = 0
        if len(chipStacks[Resource.Leather]) <= 0:
            stacksDone += 1
        if len(chipStacks[Resource.Cloth]) <= 0:
            stacksDone += 1
        if len(chipStacks[Resource.Spice]) <= 0:
            stacksDone += 1
        if len(chipStacks[Resource.Silver]) <= 0:
            stacksDone += 1
        if len(chipStacks[Resource.Gold]) <= 0:
            stacksDone += 1
        if len(chipStacks[Resource.Gem]) <= 0:
            stacksDone += 1
        if stacksDone >= 3:
            gameOver = True
        #End game check
        if gameOver:
            playerScore = sum(sum(x) for x in list(map(lambda y: list(map(lambda x: x.value, y)), playerChipStacks.values())))
            opponentScore = sum(sum(x) for x in list(map(lambda y: list(map(lambda x: x.value, y)), opponentChipStacks.values())))
            if len(camels) > len(opponentCamels):
                playerScore += 5
            elif len(opponentCamels) > len(camels):
                opponentScore += 5
            if playerScore > opponentScore:
                winner = playerName
            elif opponentScore > playerScore:
                winner = opponentName
            else:
                winner = '-'

            if firstPlayerTurn:
                p1Name = playerName
                p1Score = playerScore
                p2Name = opponentName
                p2Score = opponentScore
            else:
                p1Name = opponentName
                p1Score = opponentScore
                p2Name = playerName
                p2Score = playerScore
            description = '{}: {}, {}: {}'.format(p1Name, p1Score, p2Name, p2Score)
        priorAction = action
        priorActionDetails = actionDetails
        firstPlayerTurn = not firstPlayerTurn
    return winner, description


class GameView():
    def __init__(self, center, chipStacks, mainDeckCardsLeft,
            name, myHand, myCamels, myChipStacks,
            opponentHandCount, opponentCamelCount, opponentChipStacks, lastOpponentAction, lastOpponentActionDetails):
        #general game info
        self.center = deepcopy(center)
        self.mainDeckCardsLeft = mainDeckCardsLeft
        self.chipStacks = deepcopy(chipStacks)
        self.chipStacks[3] = len(self.chipStacks[3])
        self.chipStacks[4] = len(self.chipStacks[4])
        self.chipStacks[5] = len(self.chipStacks[5])
        #info specific to player
        self.name = name
        self.myHand = deepcopy(myHand)
        self.myCamels = myCamels
        self.myChipStacks = deepcopy(myChipStacks)
        #info about opponent
        self.opponentHandCount = opponentHandCount
        self.opponentCamelCount = opponentCamelCount
        self.opponentChipStacks = deepcopy(opponentChipStacks)
        self.opponentChipStacks[3] = len(self.opponentChipStacks[3])
        self.opponentChipStacks[4] = len(self.opponentChipStacks[4])
        self.opponentChipStacks[5] = len(self.opponentChipStacks[5])
        self.lastOpponentAction = lastOpponentAction
        self.lastOpponentActionDetails = deepcopy(lastOpponentActionDetails)
    def __str__(self):
        st = ('**************{}\'s TURN**************\n'
            '{}: {}\n'
            '{}: {}\n'
            '{}: {}\n'
            '{}: {}\n'
            '{}: {}\n'
            '{}: {}\n'
            '3x bonus ({} left); 4x bonus ({} left), 5x bonus ({} left)\n'
            '{} - {} cards remaining in Deck\n\n'
            '\t{}\'s Stuff: {} - {} camels\n'
            '\t{}: {}\n'
            '\t{}: {}\n'
            '\t{}: {}\n'
            '\t{}: {}\n'
            '\t{}: {}\n'
            '\t{}: {}\n'
            '\t3x bonus: {}; 4x bonus: {}; 5x bonus: {}\n\n'
            '\t\tOpponent\'s Stuff: {} resources - {} camels\n'
            '\t\t{}: {}\n'
            '\t\t{}: {}\n'
            '\t\t{}: {}\n'
            '\t\t{}: {}\n'
            '\t\t{}: {}\n'
            '\t\t{}: {}\n'
            '\t\t3x bonus: {} Chips; 4x bonus: {} Chips, 5x bonus: {} Chips\n'
            '\t\tLast Opponent Action: {}\n'
            '\t\tDetails: {}\n'
            .format(self.name,
                Resource.Leather.name, list(map(lambda x: x.value, self.chipStacks[Resource.Leather])),
                Resource.Cloth.name, list(map(lambda x: x.value, self.chipStacks[Resource.Cloth])),
                Resource.Spice.name, list(map(lambda x: x.value, self.chipStacks[Resource.Spice])),
                Resource.Silver.name, list(map(lambda x: x.value, self.chipStacks[Resource.Silver])),
                Resource.Gold.name, list(map(lambda x: x.value, self.chipStacks[Resource.Gold])),
                Resource.Gem.name, list(map(lambda x: x.value, self.chipStacks[Resource.Gem])),
                self.chipStacks[3], self.chipStacks[4], self.chipStacks[5],
                list(map(lambda x: x.name, self.center)), self.mainDeckCardsLeft,
                self.name, list(map(lambda x: x.name, self.myHand)), len(self.myCamels),
                Resource.Leather.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Leather])),
                Resource.Cloth.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Cloth])),
                Resource.Spice.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Spice])),
                Resource.Silver.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Silver])),
                Resource.Gold.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Gold])),
                Resource.Gem.name, list(map(lambda x: x.value, self.myChipStacks[Resource.Gem])),
                list(map(lambda x: x.value, self.myChipStacks[3])), list(map(lambda x: x.value, self.myChipStacks[4])), list(map(lambda x: x.value, self.myChipStacks[5])),
                self.opponentHandCount, self.opponentCamelCount,
                Resource.Leather.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Leather])),
                Resource.Cloth.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Cloth])),
                Resource.Spice.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Spice])),
                Resource.Silver.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Silver])),
                Resource.Gold.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Gold])),
                Resource.Gem.name, list(map(lambda x: x.value, self.opponentChipStacks[Resource.Gem])),
                self.opponentChipStacks[3], self.opponentChipStacks[4], self.opponentChipStacks[5],
                self.lastOpponentAction, self.lastOpponentActionDetails,
                ))
        return st

def checkEqual(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)
