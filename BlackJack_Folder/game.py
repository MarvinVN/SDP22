import random
from time import sleep
import RFID
import dealer

class Card:
    #initialize card with suit and rank
    def __init__(self, rank, suit, Str):
        self.rank = rank
        self.suit = suit
        self.Str = Str

    #functions to help print out card
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()

    #print card
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
    #initialize deck; used/dealt cards are taken from card to cardsused; for RFID validation and cheat prevention
    def __init__(self):
        self.cards = []
        self.cardsused = []
        self.build()

    #build deck in order
    def build(self):
        self.cards = []
        self.cardsused = []
        switch = {
            1: 'A',
            11: 'J',
            12: 'Q',
            13: 'K'
        }

        for suit in ['S', 'H', 'D', 'C']:
            for rank in range(1,14):
                if rank in switch.keys():
                    rank = switch[rank]
                self.cards.append(Card(rank,suit, str(rank)+suit))

    #currently just shuffles digital deck, can think about importing/using dealer.py here
    def shuffle(self):
        random.shuffle(self.cards)

    def scan(self, card):
        if len(self.cardsused) > 0 and card.Str == self.cardsused[-1].Str:
            print("PREVIOUS CARD READ, TRY AGAIN")
            return True
        if any(x.Str == card.Str for x in self.cardsused):
            print("CHEATING DETECTED, CARD ALREADY USED")
            while True:
                sleep(1)
        elif any(x.Str == card.Str for x in self.cards):
            print("worked")
            self.cardsused.append(card)
            return False
        else:
            print("BAD READ")
            return True

    #deals digital deck; same as above
    def deal(self, pos):
        return self.cards.pop()
        #make global
        switch = {
            'A': 1,
            'J': 11,
            'Q': 12,
            'K': 13
        }
        
        print(pos)
        if pos == 0:
            dealer.p0()
        elif pos == 1:
            dealer.p1()
        elif pos == 2:
            dealer.p2()
        elif pos == 3:
            dealer.p3()
        elif pos == 4:
            dealer.p4()

        while True:
            card = RFID.read()
            """
            while(card == False):
                tmp = ''
                if pos > 0:
                    print("Dispense failed, press hit to try again.")
                    bj_msg = Message("dispense_again", None)
                    while not tmp == 'h':
                        # tmp = button_move(pos)
                dealer.p0() #for confirmation to dispense again
                card = RFID.read()
            """
            print(card)
            rank, suit = card[:-1], card[-1]

            if rank in switch.keys():
                rank = switch[rank]

            res = Card(int(rank), suit, card)
            if self.scan(res):
                continue
            else:
                res.show()
                break

        dealer.scanConfirm() #signal that card has been scanned
        
        return res

    #calls show() on each card to print out current deck
    def show(self):
        for card in self.cards:
            print(card.show())

class Player:
    #initalize player with position number
    #TODO: once UI is realized, change wallet for user input
    def __init__(self, pos):
        self.pos = pos
        self.hand = []
        self.wallet = 1000
        self.totalBet = 0

    #draw one card from deck using deal()
    def draw(self, deck):
        card = deck.deal(self.pos)
        self.hand.append(card)

    #get money from wallet to bet
    def addBet(self, num):
        if num <= self.wallet:
            self.totalBet += num
            self.wallet -= num
        else:
            return False #will change
    
    #resets bet to 0
    def resetBet(self):
        self.totalBet = 0

    #not used, think about removing
    def allIn(self):
        self.addBet(self.wallet)
    
    #print player's hand
    def showHand(self):
        print("Player {}'s hand: {}".format(self.pos, self.hand))