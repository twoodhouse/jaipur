# jaipur
Python jaipur simulator

My apologies for the low code quality in the main jaipur.py file. This was intended to be a rapid development experiment.

Rules: http://www.yucata.de/en/Rules/Jaipur
Modifications to rules: no tie break condition included. A point tie is considered a tie.
Only one round is played per game, rather than up to 3.

Rules for creating strategies:
1. No accessing higher-level namespace variables. Work within the strategy class you are making and the gameView passed to each function in the interface. Didn't have time to make common game variables fully private, so no hacking to see your opponent's cards.
2. Make sure you fully implement the function interface shown in the example strategies

How to play using the InteractiveStrategy mode (this lets the user take on one or both of the gameplay roles):
- When choosing an action, always type precisely one of these four action options: TakeCard, TradeCards, TakeCamels, PlayCards
- After an action is chosen, additional prompts may ask the number of items to play or the specific resources played. When answering a query about resources, answer with the capitalized name of the resource (Leather, Cloth, Spice, Silver, Gold, or Gem)
- If you mistype, the code will raise an exception and stop. I didn't have time to make the interface nice, as this was mainly for ensuring all the rules work correctly.
- If you do something illegal, you will be disqualified in the match, just like the automated strategies can be disqualified. Make sure the action you are claiming for your turn is fully legal.
