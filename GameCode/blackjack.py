import RPi.GPIO as GPIO
from time import sleep
from gameState import gameState
import test

buttons = {
    "hit": 19,
    "stand": 26
}

pin_list = [16,20,21]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(list(buttons.values()), GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

def main():
    gs = gameState(1) #initialize gamestate
    while(1):   #main game loop
        totals = [] #list of hand totals
        gs.setPlayers((int)(input("How many people are playing?\n")))
        gs.resetHands()
        gs.deck.build()
        gs.deck.shuffle()

        print("Shuffling...")
        test.shuffle()

        gs.dealCards(2) #arg = num of cards
        sleep(2)

        print("Dealing...")
        test.p1()
        test.p2()

        test.p1()
        test.p2()

        totals.append(0) #temp dealer score; needs to be calculated after players
        for x in range(1, gs.numPlay): #Player turns
            totals.append(playerTurn(gs.players[x], gs.deck))
        totals[0] = dealerTurn(gs.players[0], gs.deck) #dealer turn
        score(gs.players, totals)

        gs.showWallets() #debugging purposes
        
        print("Play again? (hit for yes, stand for no)\n")
        play_again = button_move()
        if play_again == "h":
            continue
        elif play_again == "s":
            GPIO.cleanup()
            quit() #temporary, should go back to menu screen
        else:
            print("\n Invalid answer, quitting.")
            quit() #same as above

#takes in the player and deck as args, returns the value of player's hand    
def playerTurn(player, deck):
    move = ''
    bet = (int) (input("How much do you want to bet? Current wallet = {}\n".format(player.wallet)))
    player.addBet(bet) #handle invalid inputs (if bet > wallet, if no number is given <-- this one shouldnt be a problem when GUI is in place)
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
            move = button_move()
            if move == 'h':
                player.draw(deck, 1)
                test.p2()

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
            test.p1()
        sleep(1)
    return total

#change for multi-players when buttons are set up
def button_move():
    move = ""
    GPIO.add_event_detect(buttons["hit"], GPIO.FALLING, bouncetime=500)
    GPIO.add_event_detect(buttons["stand"], GPIO.FALLING, bouncetime=500)
    while True:
        sleep(.01)
        if GPIO.event_detected(buttons["hit"]):
            move =  'h'
            break
        elif GPIO.event_detected(buttons["stand"]):
            move =  's'
            break
        
    GPIO.remove_event_detect(buttons["hit"])
    GPIO.remove_event_detect(buttons["stand"])
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