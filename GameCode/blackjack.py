import RPi.GPIO as GPIO
from time import sleep
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

from gameState import gameState
import dealer

#input pins and their corresponding roles/players
player_buttons = {
    1: {"hit": 2, "stand": 3, "double": 4},
    2: {"hit": 14, "stand": 15, "double": 18},
    3: {"hit": 17, "stand": 27, "double": 22},
    4: {"hit": 23, "stand": 24, "double": 25}
    }

#categorize pins for setup
input_pins = [x for pins in player_buttons.values() for x in pins.values()]
output_pins = [5,13,16,20,21]
#5 for RFID, 13 for confirm, [16,20,21] for ATmega comm.

# Hardware setup (RPi GPIO and RFID)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(input_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(output_pins, GPIO.OUT, initial=GPIO.LOW)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()

def main():

    dealer.scanConfirm()

    gs = gameState(1)
    gs.deck.build()

    dealer.shuffle()

    #main game loop
    while(1):
        totals = []
        players = 1
        x = ''
        print("How many people are playing?")
        while(True):
            print(f"Players: {players}")
            x = button_move(1)
            print(x)
            if x == 'h' and players < 4:
                players += 1
            elif x == 's' and players > 1:
                players -= 1
            elif x == 'd':
                break

        gs.setPlayers(players)
        gs.resetHands()

        if gs.checkCardCount():
            tmp = 's'
            print("Not enough cards, please load cards into shuffler and press (hit) button")
            while(not tmp == 'h'):
                tmp = button_move(1)
            dealer.shuffle()    

        for x in range(1, gs.numPlay):
            playerBet(gs.players[x])

        print("Dealing...")
        gs.dealCards()
        
        totals.append(0) #temp dealer score; will be calculated after players' turn
        for x in range(1, gs.numPlay):
            totals.append(playerTurn(gs.players[x], gs.deck))
        totals[0] = dealerTurn(gs.players[0], gs.deck)

        score(gs.players, totals)
        gs.showWallets()
        
        print("Play again? (hit for yes, stand for no)\n")
        play_again = button_move(1) #player 1 decides to continue the game
        if play_again == "h":
            continue
        elif play_again == "s":
            GPIO.cleanup()
            quit() #should go to menu screen once GUI implemented

def playerBet(player):
    move = ''
    bet = 10
    print(f"How much does Player {player.pos} want to bet? Current wallet = {player.wallet}")
    while(move != 'd'):
        print(f"Bet: {bet}")
        move = button_move(player.pos)
        if move == 'h' and bet < player.wallet:
            bet += 10
        elif move == 's' and bet > 10:
            bet -= 10
        elif move == 'd':
            break    
    player.addBet(bet) 

#takes in the player and deck as args, returns the value of player's hand    
def playerTurn(player, deck):
    move = ''
    print(f"Player {player.pos}'s Turn! Bet Amount = {player.totalBet}")
    while move != 's':  #player move loop
        total = checkValue(player.hand)
        player.showHand()
        print("Total value: {}".format(total))

        sleep(.5)

        if total > 21:
            print("Bust!")
            break
        elif total == 21:
            print("21!")
            break
        else:
            print("Do you want to hit or stand (h/s)?")
            move = button_move(player.pos)
            if move == 'h':
                player.draw(deck)

    return total

#same as above; follows blackjack dealer rules
def dealerTurn(player, deck):
    total = 0
    while total < 17:
        total = checkValue(player.hand)
        player.showHand()
        print(": {}".format(total))
        if total >= 17:
            break
        else:
            player.draw(deck)
        sleep(1)
    return total

def button_move(pos):
    player_buttons = {
    1: {"hit": 2, "stand": 3, "double": 4},
    2: {"hit": 14, "stand": 15, "double": 18},
    3: {"hit": 17, "stand": 27, "double": 22},
    4: {"hit": 23, "stand": 24, "double": 25}
    }

    move = ""
    hit, stand, double = player_buttons[pos]["hit"], player_buttons[pos]["stand"], player_buttons[pos]["double"]
    
    GPIO.add_event_detect(hit, GPIO.FALLING, bouncetime=500)
    GPIO.add_event_detect(stand, GPIO.FALLING, bouncetime=500)
    GPIO.add_event_detect(double, GPIO.FALLING, bouncetime=500)

    while True:
        sleep(.2)
        if GPIO.event_detected(hit):
            move = 'h'
            break
        elif GPIO.event_detected(stand):
            move = 's'
            break
        elif GPIO.event_detected(double):
            move = 'd'
            break
        else:
            move = ''
            continue

    GPIO.remove_event_detect(hit)
    GPIO.remove_event_detect(stand)
    GPIO.remove_event_detect(double)

    return move

#takes a player's hand; returns value
def checkValue(hand):
    val = 0
    #sort and add Aces last so choose between 1/11 values
    hand.sort(key=lambda x: x.rank, reverse=True)
    for x in hand:
        if x.rank in [13, 12, 11]: #K, Q, J
            val += 10
        elif x.rank == 1: #Ace
            if val >= 11:
                val += 1
            else:
                val += 11
        else:
            val += x.rank
    return val

def score(players, totals):
    dealer_score = totals[0]
    print("Totals: {}".format(totals))
    if dealer_score > 21:
        for x in range(1, len(players)):
            if totals[x] > 21:
                settleBet(players[x], -1)
            elif totals[x] == 21:
                settleBet(players[x], 2)
            else:
                settleBet(players[x], 1)
    elif dealer_score == 21:
        for x in range(1, len(players)):
            if totals[x] == 21:
                settleBet(players[x], 0)
            else:
                settleBet(players[x], -1)
    else:
        for x in range(1, len(players)):
            if totals[x] < dealer_score or totals[x] > 21:
                settleBet(players[x], -1)
            elif totals[x] == dealer_score:
                settleBet(players[x], 0)
            elif totals[x] == 21:
                settleBet(players[x], 2)
            else:
                settleBet(players[x], 1)

#system pays out 2 to 1, 2.5 to 1 for hitting blackjack
#res: 1=win, 0=tie, -1=loss
def settleBet(player, res):
    if res == 2:
        player.wallet += player.totalBet * 2.5
    elif res == 1:
        player.wallet += player.totalBet * 2
    elif res == 0:
        player.wallet += player.totalBet
    #if player loses, bet is just reset
    player.resetBet()

if __name__ == "__main__":
    main()