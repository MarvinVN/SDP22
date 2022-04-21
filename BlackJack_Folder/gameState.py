from game import Card, Deck, Player

class gameState:
    #initialize gamestate with number of players
    def __init__(self, numPlay, gameMode, userInput):
        self.numPlay = 0
        self.players = []
        self.deck = Deck()
        self.setPlayers(numPlay)
        self.gameMode = gameMode
        self.userInput = userInput

    #set amount of players for current game
    def setPlayers(self, numPlay):
        if numPlay not in [1, 2, 3, 4]:
            return False 

        prevNum = self.numPlay
        self.numPlay = numPlay + 1 #plus 1 needed for dealer

        #player(index) 0 reserved for dealer, 1-4 for users
        if prevNum < self.numPlay: #if more players than previous game, initialize players
            for x in range(prevNum, self.numPlay):
                self.players.append(Player(x)) 
        elif prevNum > self.numPlay: #if less players than previous game, remove players. Currently removes players from 4 to 1, should be changed later
            for x in range(prevNum-self.numPlay):
                self.players.pop() 

    #return player's hand
    def getPlayerHand(self, player):
        return self.players[player].hand

    #resets all players' hands
    def resetHands(self):
        for x in self.players:
            x.hand = []

    #prints all players' hands
    def showAllHands(self):
        for x in self.players:
            x.showHand()

    #returns all players' bets
    def getBets(self): 
        bets = [0] #dealer doesn't bet, set at 0
        for x in self.players:
            bets.append(x.getTotalBet)
        return bets

    #resets all players' bets
    def resetBets(self):
        for x in self.players:
            x.resetBet()
    
    #prints all players' wallets
    def showWallets(self):
        wallets = []
        for x in self.players:
            wallets.append(x.wallet)
        print(wallets)

    #deal 2 cards to all players
    def dealCards(self):
        for _ in range(2):
            for x in range(self.numPlay):
                self.players[x].draw(self.deck)

    def checkCardCount(self):
        target = 52 - (self.numPlay * 3)
        if len(self.deck.cardsused) > target:
            return True
        return False