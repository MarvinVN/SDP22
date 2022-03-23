import RPi.GPIO as GPIO
from time import sleep
from gameState import gameState
import dealer

#input pins and their corresponding roles/players
player_buttons = {
    1: {"hit": 19, "stand": 26}
}

#categorize pins for setup
input_pins = [x for pins in player_buttons.values() for x in pins.values()]
output_pins = [16,20,21]

# RPi GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(input_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(output_pins, GPIO.OUT, initial=GPIO.LOW)

def main():
    gs = gameState(1) #initialize gamestate
    while(1):   #main game loop
        totals = [] #list of hand totals

        #set up gamestate
        gs.setPlayers((int)(input("How many people are playing?\n")))
        gs.resetHands()
        gs.deck.build() #TODO: put outside of gameloop when implementing forced shuffle (no more cards)

        gs.deck.shuffle()
        print("Shuffling...")
        dealer.shuffle()

        sleep(2)

        gs.dealCards(2) #arg = num of cards
        print("Dealing...")
        dealer.init_deal() #need to be adjusted for 1-3 players

        totals.append(0) #temp dealer score; needs to be calculated after players

        #loop through players turns
        for x in range(1, gs.numPlay):
            totals.append(playerTurn(gs.players[x], gs.deck))

        #dealer turn
        totals[0] = dealerTurn(gs.players[0], gs.deck)

        score(gs.players, totals)

        gs.showWallets() #debugging purposes
        
        print("Play again? (hit for yes, stand for no)\n")
        play_again = button_move(1) #player 1 decides to continue the game
        if play_again == "h":
            continue
        elif play_again == "s":
            GPIO.cleanup()
            quit() #should go to menu screen once GUI implemented

#takes in player.pos to physically deal a card to the appropriate player
def playerDraw(pos):
    if pos == 0:
        dealer.p1()
    elif pos == 1:
        dealer.p2()
    elif pos == 2:
        dealer.p3()
    elif pos == 3:
        dealer.p4()
    elif pos == 4:
        dealer.p5()

#takes in the player and deck as args, returns the value of player's hand    
def playerTurn(player, deck):
    move = ''
    bet = (int) (input("How much do you want to bet? Current wallet = {}\n".format(player.wallet)))
    player.addBet(bet) 
    while move != 's':  #player move loop
        total = checkValue(player.hand)
        player.showHand()   #display cards in GUI
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
                player.draw(deck, 1)
                playerDraw(player.pos)

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
            player.draw(deck, 1)
            sleep(3)
            playerDraw(0)
        sleep(1)
    return total

#change for multi-players when buttons are set up
def button_move(pos):
    move = ""
    hit, stand = player_buttons[pos]["hit"], player_buttons[pos]["stand"]
    
    GPIO.add_event_detect(hit, GPIO.FALLING, bouncetime=500)
    GPIO.add_event_detect(stand, GPIO.FALLING, bouncetime=500)

    while True:
        sleep(.01)
        if GPIO.event_detected(hit):
            move =  'h'
            break
        elif GPIO.event_detected(stand):
            move =  's'
            break
        
    GPIO.remove_event_detect(hit)
    GPIO.remove_event_detect(stand)

    return move

#takes a player's hand; returns value
def checkValue(hand):
    val = 0
    for x in hand:
        if x.rank in [13, 12, 11]: #K, Q, J
            val += 10
        elif x == 1: #Ace
            if val >= 11:
                val += 1
            else:
                val += 11
        else:
            val += x.rank
    return val

#takes in players and totals; handles resulting win/losses --> will need to clean up later
def score(players, totals):
    dealer_score = totals[0]
    print("Totals: {}".format(totals)) #debug
    if dealer_score > 21:
        for x in range(1, len(players)):
            if totals[x] > 21:
                settleBet(players[x], -1)
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
            else:
                settleBet(players[x], 1)

#system pays out 2 to 1
#res: 1=win, 0=tie, -1=loss
def settleBet(player, res):
    if res == 1:
        player.wallet += player.totalBet * 2
    elif res == 0:
        player.wallet += player.totalBet
    #if player loses, bet is just reset
    player.resetBet()

if __name__ == "__main__":
    main()