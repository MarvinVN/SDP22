from game import *

class gameState:
    def __init__(self, numPlay):
        if numPlay not in [1, 2, 3, 4]:
            return False #might need to change behavior
        else:
            self.numPlay = numPlay
            self.players = []
            self.deck = Deck()
            self.startGame(numPlay)

    def startGame(self, numPlay):
        for x in range(1, numPlay):
            self.players[x] = Player(x) #player 0 reserved for dealer, 1-4 for users    