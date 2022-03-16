import random
import serial
import time

class Card:
    #initialize card with suit and rank
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
        """
        for suit in ['S', 'H', 'D', 'C']:
            for rank in range(1,14):
                if rank == 1:
                    rank = "A"
                elif rank == 11:
                    rank = "J"
                elif rank == 12:
                    rank = "Q"
                elif rank == 13:
                    rank = "K"
                self.cards.append("{}{}".format(rank,suit))
        """
        for suit in ['s', 'h', 'd', 'c']:
            for rank in range(1,14):
                self.cards.append(Card(rank,suit))

    #currently just shuffles digital deck, can think about importing/using dealer.py here
    def shuffle(self):
        """
        print("Shuffling")
        port = '/dev/cu.usbserial-1410'
        baudrate = 115200
        x = '0'
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        ser.write(bytes(x, 'utf-8'))
        time.sleep(6)     
        #shuffle the deck
        """
        random.shuffle(self.cards)

    #deals digital deck; same as above
    def deal(self):
        """data = self.RFID()
        if data != '':
            data = data.split('\r')
            self.cardsused.append(data[0])
            self.cards.remove(data[0])
            return data[0]
        """
        return self.cards.pop()

    #TODO: integrate libnfc with this function or with deal function
    def RFID(self):
        port = '/dev/cu.usbserial-1410'
        baudrate = 115200
        ser = serial.Serial(port,baudrate,timeout=1)
        x = '1'
        data = ''
        print("waiting for Card")
        while len(data) < 1 or data in self.cardsused:
            try:
                time.sleep(2)
                ser.write(bytes(x, 'utf-8'))
                time.sleep(2)
                data = ser.readline().decode()
            except:
                print("Error")
        if len(data) > 2:
            print(data)
            print("CHEATING DECTECTED")
            while True:
                time.sleep(1)
        else:
            print(data)
        return data

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

    #draw from deck using deal()
    def draw(self, deck, num):
        for x in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else:
                return False
        return True

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