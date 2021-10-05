from game import *
from gameState import *

gs = gameState(1)
gs.dealCards(2)
gs.showAllHands()

gs.restartGame(True)
gs.getPlayerHand(0)

gs.restartGame(False)
gs.deck.shuffle()
gs.dealCards(2)
gs.showAllHands()