from game import *

class gameState:
    def __init__(self, numPlay):
        if numPlay not in [1, 2, 3, 4]:
            return False #might need to change behavior
        else:
            self.numPlay = numPlay + 1 #plus 1 needed for dealer
            self.players = []
            self.deck = Deck()
            self.startGame(self.numPlay)

    def startGame(self, numPlay):
        if numPlay-1 not in [1, 2, 3, 4]: #again, behavior will need to be changed; num-1 needed for restart
            return False

        self.players = []
        for x in range(numPlay):
            self.players.append(Player(x)) #player 0 reserved for dealer, 1-4 for users

    def restartGame(self, samePlayers):
        if samePlayers == True:
            self.deck.build()
        else:
            self.numPlay = int(input("How many people are playing?")) + 1
            self.startGame(self.numPlay)

    def getPlayerHand(self, player):
        return self.players[player].hand

    def showAllHands(self): #debugging purposes
        for x in self.players:
            x.showHand()

    def getBets(self): 
        bets = [0] #dealer doesn't bet, set at 0
        for x in self.players:
            bets.append(x.getTotalBet)
        return bets

    def resetBets(self):
        for x in self.players:
            x.resetBet()

    def dealCards(self, num):
        for x in range(self.numPlay):
            self.players[x].draw(self.deck, num)