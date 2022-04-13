from game import Card, Deck, Player
import blackjack_globals

class gameState:
    def __init__(self, numPlay, gameMode, userInput):
        self.numPlay = 0
        self.players = []
        self.deck = Deck()
        self.setPlayers(numPlay)
        self.gameMode = gameMode
        self.userInput = userInput

    def setPlayers(self, numPlay):
        prevNum = self.numPlay
        self.numPlay = numPlay + 1 #plus 1 needed for dealer

        #player 0 reserved for dealer, 1-4 for users
        if prevNum < self.numPlay: #if more players than previous game, initialize players
            for x in range(prevNum, self.numPlay):
                self.players.append(Player(x)) 
        elif prevNum > self.numPlay: #if less players than previous game, remove players. Currently removes players from 4 to 1, should be changed later
            for x in range(prevNum-self.numPlay):
                self.players.pop() 
        print(self.players)

    def getPlayerHand(self, player):
        return self.players[player].hand

    # maybe use this to reset hands?
    def resetHands(self):
        for x in self.players:
            x.hand = []
 
    def showAllHands(self):
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

    def getWallets(self):
        wallets = []
        for x in self.players:
            wallets.append(x.wallet)
        return wallets
    
    def showWallets(self):
        wallets = []
        for x in self.players:
            wallets.append(x.wallet)
        print(wallets)

    def dealCards(self, num):
        for x in range(self.numPlay):
            self.players[x].draw(self.deck, num)
