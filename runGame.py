#!/usr/bin/python3.5
from randomStrategy import RandomStrategy
from randomStrategy2 import RandomStrategy2
from interactiveStrategy import InteractiveStrategy
from jaipur import runJaipur

p1 = RandomStrategy()
p2 = RandomStrategy2()

p1Wins = 0
winner, desc = runJaipur((p1, p2))
print(winner)
print(desc)
