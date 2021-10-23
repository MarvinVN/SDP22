import random

#in full implementation, RFID will be scanned and looked up in dictionary for suit/rank
#think about ways to do this...
class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    #functions to help print out card
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()

    def show(self):
        if self.rank == 1:
            rank = "A"
        elif self.rank == 11:
            rank = "J"
        elif self.rank == 12:
            rank = "Q"
        elif self.rank == 13:
            rank = "K"
        else:
            rank = self.rank

        return "{}{}".format(rank, self.suit)

class Deck:  
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        self.cards = []
        for suit in ['s', 'h', 'd', 'c']:
            for rank in range(1,14):
                self.cards.append(Card(rank, suit))

    #will talk to shuffler
    def shuffle(self):
        random.shuffle(self.cards)

    #will talk to dealer
    def deal(self):
        return self.cards.pop()

    def show(self):
        for card in self.cards:
            print(card.show())

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.hand = []
        self.wallet = 1000 #will be user input
        self.totalBet = 0

    def draw(self, deck, num):
        for x in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else:
                return False #unlikely event, but figure out what to do here anyways
        return True

    #get money from wallet to bet
    def addBet(self, num):
        if num <= self.wallet:
            self.totalBet += num
            self.wallet -= num
        else:
            return False #will change
    
    def resetBet(self):
        self.totalBet = 0

    def allIn(self):
        self.addBet(self.wallet)

    def showHand(self):
        print("Player {}'s hand: {}".format(self.pos, self.hand))