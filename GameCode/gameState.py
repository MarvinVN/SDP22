from . import Card, Deck, Player

class gameState:
    def __init__(self, numPlay):
        self.numPlay = 0
        self.players = []
        self.deck = Deck()
        self.setPlayers(numPlay)

    def setPlayers(self, numPlay):
        if numPlay not in [1, 2, 3, 4]:
            return False #might need to change behavior... probably not; just make it 4 buttons

        prevNum = self.numPlay
        self.numPlay = numPlay + 1 #plus 1 needed for dealer

        #player(index) 0 reserved for dealer, 1-4 for users
        if prevNum < self.numPlay: #if more players than previous game, initialize players
            for x in range(prevNum, self.numPlay):
                self.players.append(Player(x)) 
        elif prevNum > self.numPlay: #if less players than previous game, remove players. Currently removes players from 4 to 1, should be changed later
            for x in range(prevNum-self.numPlay):
                self.players.pop() 

    def getPlayerHand(self, player):
        return self.players[player].hand

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
    
    def showWallets(self):
        wallets = []
        for x in self.players:
            wallets.append(x.wallet)
        print(wallets)

    def dealCards(self, num):
        for x in range(self.numPlay):
            self.players[x].draw(self.deck, num)