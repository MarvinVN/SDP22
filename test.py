from blackjack import *

gs = gameState((int)(input("How many people are playing?")))
gs.deck.shuffle()
gs.dealCards(2)

for x in range(1, gs.numPlay):
    print(x)