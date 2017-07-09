# jaipur
Python jaipur simulator

My apologies for the low code quality in the main jaipur.py file. This was intended to be a rapid development experiment.

Rules: http://www.yucata.de/en/Rules/Jaipur
Modifications to rules: no tie break condition included. A point tie is considered a tie.
Only one round is played per game, rather than up to 3.

Rules for creating strategies:
1. No accessing higher-level namespace variables. Work within the strategy class you are making and the gameView passed to each function in the interface. Didn't have time to make common game variables fully private, so no hacking to see your opponent's cards.
2. Make sure you fully implement the function interface shown in the example strategies

## The Strategy interface
The strategy interface is simply four methods that the Strategy class must contain. Note this is not a formal python interface.

actionChoice(self, gameView) - Return one of the four Action Enum values. The value returned is used by the game function to call the correct additional function in your strategy class. For example, if you return Action.TakeCard when actionChoice() is called, then the game will later call takeCardChoice() to retrieve the card you want to take from the center.

takeCardChoice(self, gameView) - Return one of the Resource Enum values. (Remember that taking a camel here will disqualify you. Only take camels using the TakeCamels action - taking only a single camel when more are available is not allowed according to the rules).

tradeCardsChoice(self, gameView) - Return a two-valued tuple. The first value is a list of Resource Enum values to move to the center cards from your hand. The second value is a list of Resource Enum values to take from the center cards. (Remember you can't take any of the same resource types that you laid out).

playCardsChoice(self, gameView) - Return a list of Resource Enum values. Remember they must all be the same value to avoid disqualification. Additionally you must play at least two if playing down gold, silver, or gem.

As a general note, the system will disqualify you if you do something that doesn't make sense, like trying to play down three gem cards if you only have one.

## Interactive Strategy
How to play using the InteractiveStrategy mode (this lets the user take on one or both of the gameplay roles):
- When choosing an action, always type precisely one of these four action options: TakeCard, TradeCards, TakeCamels, PlayCards
- After an action is chosen, additional prompts may ask the number of items to play or the specific resources played. When answering a query about resources, answer with the capitalized name of the resource (Leather, Cloth, Spice, Silver, Gold, or Gem)
- If you mistype, the code will raise an exception and stop. I didn't have time to make the interface nice, as this was mainly for ensuring all the rules work correctly.
- If you do something illegal, you will be disqualified in the match, just like the automated strategies can be disqualified. Make sure the action you are claiming for your turn is fully legal.

## GameView info sent to strategies
See the GameView class to get an idea of the information included in each request to the strategy for information. Here is a print of one such class passed to a strategy (unfortunately, this is not sorted nicely).

Note that the "chipStacks", "myChipStacks", and "opponentChipStacks" dictionaries have a key for each resource type (and additionally the keys 3, 4, and 5 to represent the bonus chips gained from sets of 3, 4, or 5 cards. In the opponent chip stack, the actual value of the bonus tokens are not sent (since these are not visible to the player). Instead, only the number of bonus tokens is available.

{
	'opponentChipStacks': { < Resource.Gold: 4 >: [ < util.Chip object at 0x7b442ede3748 > , < util.Chip object at 0x7b442ede3f98 > ],
		3: 0,
		4: 0,
		< Resource.Spice: 2 >: [ < util.Chip object at 0x7b442ede3eb8 > , < util.Chip object at 0x7b442ede3e80 > ],
		< Resource.Leather: 0 >: [ < util.Chip object at 0x7b442ede33c8 > , < util.Chip object at 0x7b442ede36a0 > , < util.Chip object at 0x7b442ede3b70 > , < util.Chip object at 0x7b442ede9588 > ],
		< Resource.Cloth: 1 >: [ < util.Chip object at 0x7b442ede9748 > , < util.Chip object at 0x7b442ede9128 > , < util.Chip object at 0x7b442ede9198 > , < util.Chip object at 0x7b442ede97b8 > , < util.Chip object at 0x7b442ede90f0 > ],
		< Resource.Silver: 3 >: [],
		< Resource.Gem: 5 >: [],
		5: 0
	},
	'lastOpponentActionDetails': < Resource.Spice: 2 > ,
	'name': 'P2',
	'center': [ < Resource.Spice: 2 > , < Resource.Spice: 2 > , < Resource.Leather: 0 > , < Resource.Camel: 6 > , < Resource.Gem: 5 > ],
	'myChipStacks': { < Resource.Gold: 4 >: [ < util.Chip object at 0x7b442ede3978 > , < util.Chip object at 0x7b442ede3588 > , < util.Chip object at 0x7b442ede3be0 > ],
		3: [ < util.Chip object at 0x7b442ede3630 > ],
		4: [],
		< Resource.Spice: 2 >: [ < util.Chip object at 0x7b442ede3f60 > , < util.Chip object at 0x7b442ede3550 > ],
		< Resource.Leather: 0 >: [ < util.Chip object at 0x7b442ede3a90 > , < util.Chip object at 0x7b442ede3b00 > , < util.Chip object at 0x7b442ede34a8 > , < util.Chip object at 0x7b442ede34e0 > ],
		< Resource.Cloth: 1 >: [ < util.Chip object at 0x7b442ede3c50 > , < util.Chip object at 0x7b442ede39b0 > ],
		< Resource.Silver: 3 >: [ < util.Chip object at 0x7b442ede3d68 > , < util.Chip object at 0x7b442ede3ac8 > , < util.Chip object at 0x7b442ede3d30 > ],
		< Resource.Gem: 5 >: [ < util.Chip object at 0x7b442ede3cf8 > , < util.Chip object at 0x7b442ede36d8 > , < util.Chip object at 0x7b442ede3668 > , < util.Chip object at 0x7b442ede3860 > ],
		5: []
	},
	'lastOpponentAction': < Action.TakeCard: 0 > ,
	'myHand': [ < Resource.Silver: 3 > , < Resource.Silver: 3 > , < Resource.Spice: 2 > , < Resource.Silver: 3 > , < Resource.Leather: 0 > ],
	'chipStacks': { < Resource.Gold: 4 >: [],
		3: 6,
		4: 6,
		< Resource.Spice: 2 >: [ < util.Chip object at 0x7b442ede3f28 > , < util.Chip object at 0x7b442ede38d0 > , < util.Chip object at 0x7b442ede3898 > ],
		< Resource.Leather: 0 >: [ < util.Chip object at 0x7b442ede3b38 > ],
		< Resource.Cloth: 1 >: [],
		< Resource.Silver: 3 >: [ < util.Chip object at 0x7b442ede35f8 > , < util.Chip object at 0x7b442ede39e8 > ],
		< Resource.Gem: 5 >: [ < util.Chip object at 0x7b442ede3da0 > ],
		5: 5
	},
	'opponentHandCount': 2,
	'mainDeckCardsLeft': 0,
	'myCamels': [],
	'opponentCamelCount': 10
}
