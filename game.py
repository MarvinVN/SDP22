import random
import serial
import time
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
        self.cardsused = []
        self.build()

    def build(self):
        self.cards = []
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

    #will talk to shuffler
    def shuffle(self):
        print("Shuffling")
        port = '/dev/cu.usbserial-1410'
        baudrate = 115200
        x = '0'
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        ser.write(bytes(x, 'utf-8'))
        time.sleep(6)     
        #shuffle the deck

    #will talk to dealer
    def deal(self):
        data = self.RFID()
        if data != '':
            data = data.split('\r')
            self.cardsused.append(data[0])
            self.cards.remove(data[0])
            return data[0]

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