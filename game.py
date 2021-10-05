import random

class Card:

    #rank = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    #suit = ['s', 'h', 'd', 'c']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

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

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def show(self):
        for card in self.cards:
            print(card.show())

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.hand = []

    def draw(self, deck, num):
        for x in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else:
                return False
        return True

    def showHand(self):
        print("Player {}'s hand: {}".format(self.pos, self.hand))