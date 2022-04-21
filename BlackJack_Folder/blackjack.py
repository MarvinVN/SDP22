import RPi.GPIO as GPIO
import time

import board
import busio
from blackjack_globals import Message
# from digitalio import DigitalInOut
# from adafruit_pn532.spi import PN532_SPI
from gameState import gameState
import dealer

#categorize pins for setup
output_pins = [5,13,16,20,21]
#5 for RFID, 13 for confirm, [16,20,21] for ATmega comm.

# Hardware setup (RPi GPIO and RFID)
# GPIO.cleanup()
# GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(output_pins, GPIO.OUT, initial=GPIO.LOW)

# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# cs_pin = DigitalInOut(board.D5)
# pn532 = PN532_SPI(spi, cs_pin, debug=False)
# pn532.SAM_configuration()

def blackjack_process(gui_to_bj_queue, bj_to_gui_queue):
    t1 = time.time()
    t2 = time.time()

    done_game = False
    rounds = 0
    wins_list = [0,0,0,0,0]
    winner = [False, False, False, False, False]
    alt_winner = [False, False, False, False, False]
    game_duration = 0 # keep track of length of game
    initial_round = True
    round_score = []
    numPlayers = ""

    dealer.scanConfirm()

    gameMode = " "
    userInput = 0
    gs = gameState(1, gameMode, userInput)

    #main game loop
    while(1):
        print("entered the start of a round loop")
        totals = []
        #players = 1

        if initial_round:
            msg = gui_to_bj_queue.get()

        if msg.id == "game_start":
            print("BJ in initial round...")
            initial_round = False
            numPlayers = msg.content[0]
            playerWallets = msg.content[1]
            bet = msg.content[2]
            gameMode = msg.content[3]
            gs.userInput = msg.content[4]
        
            player_msg = start_game(gs, numPlayers, playerWallets, bet, gameMode, gs.userInput, gui_to_bj_queue)
            # sending initial player cards to GUI
            for x in player_msg:
                print("entered player_msg: ", x)
                bj_to_gui_queue.put(x)
            msg = Message("None", None)
        print("BJ about to append to totals...")
        totals.append(0) #temp dealer score; will be calculated after players' turn
        # one full round of players
        for x in range(1, gs.numPlay):
            print("BJ entering player turn...")
            totals.append(playerTurn(gs.players[x], gs.deck, numPlayers,
                gui_to_bj_queue, bj_to_gui_queue))

        totals[0] = dealerTurn(gs.players[0], gs.deck)

        # saving the round score to update gui
        round_score = score(gs.players, totals)
        gs.showWallets()
        print("done round, sending to gui....")

        # finished one round, inform gui
        bj_msg = Message("done_round", [gs.players[0].hand, round_score, gs.getWallets(), gs.checkCardCount()])
        bj_to_gui_queue.put(bj_msg)
        #print("sent msg to gui: ", bj_msg[0], bj_msg[1], bj_msg[2], bj_msg[3])
        print("sent msg to gui: " + bj_msg.id)

        # checking game end states
        t2 = time.time()
        game_duration = (t2 - t1) / 60 # convert seconds to minutes
        rounds = rounds + 1

        for x in range(1, gs.numPlay):
            if checkValue(gs.players[x].hand) > checkValue(gs.players[0].hand) and checkValue(gs.players[x].hand) <= 21:
                wins_list[x] = wins_list[x] + 1
            elif checkValue(gs.players[0].hand) > 21:
                wins_list[x] = wins_list[x] + 1

            if gs.gameMode == "Winning Amount":
                if gs.players[x].wallet >= gs.userInput:
                    done_game = True
                    winner[x] = True
            elif gs.gameMode == "Number of Wins":
                if wins_list[x] == gs.userInput:
                    done_game = True
                    winner[x] = True
            elif gs.gameMode == "Total Games":
                if rounds == gs.userInput:
                    done_game = True
                    if gs.players[x].wallet == max(gs.getWallets()):
                        winner[x] = True # winners for most money
                    if wins_list[x] == max(wins_list):
                        alt_winner[x] = True # winners for most number of wins
            elif gs.gameMode == "Duration":
                if game_duration >= gs.userInput:
                    done_game = True
                    if gs.players[x].wallet == max(gs.getWallets()):
                        winner[x] = True # winners for most money
                    if wins_list[x] == max(wins_list):
                        alt_winner[x] = True # winners for most number of wins
            else:
                pass

        gs.resetHands()
        print("reset hands after a round completes")
        # checking if the game has ended (given the end state)
        if done_game: # send over winner's winning information (two winner lists)
            bj_msg = Message("GAME OVER!", [winner, alt_winner, gs.getWallets(), wins_list])
            bj_to_gui_queue.put(bj_msg)
        # check if the deck is empty
        elif gs.checkCardCount():
            print("entered checkCardCount")
            waiting_for_msg = True
            # wait for confirmation from GUI that "hit" button was pressed, and we can shuffle the cards
            while(waiting_for_msg):
                msg = gui_to_bj_queue.get()
                if msg.id == "hit":
                    waiting_for_msg = False
            # TODO:
            # 1. send msg to GUI, display message
            # 2. receive msg from GUI
            # 3. check message for confirm button to re-load
            dealer.shuffle()

        gs.dealCards()

        for x in range(gs.numPlay):
            gs.players[x].resetBet()
            gs.players[x].addBet(bet)

            bj_msg = Message("p" + str(x) + "_cards", gs.players[x].hand)
            bj_to_gui_queue.put(bj_msg)

        if not done_game:
            bj_msg = Message("continue", None)
            bj_to_gui_queue.put(bj_msg)

def start_game(gs, numPlayers, playerAmount, bet, gameMode, userInput, gui_to_bj_queue):
    # making msg list for each player
    msg = []

    gs.deck.build()
    gs.deck.shuffle()
    gs.setPlayers(int(numPlayers))
    gs.userInput = userInput
    gs.gameMode = gameMode
    gs.resetHands()

    # checking the number of cards used vs cards left
    #if gs.checkCardCount():
    waiting_for_msg = True
    # wait for confirmation from GUI that "hit" button was pressed, and we can shuffle the cards
    while(waiting_for_msg):
        bj_msg = gui_to_bj_queue.get()
        if bj_msg.id == "hit":
            waiting_for_msg = False
            print("bj received hit for shuffle....")

    print("Shuffling initial shuffle....")
    dealer.shuffle()    

    print("Dealing...")
    gs.dealCards()

    for x in range(gs.numPlay):
        gs.players[x].wallet = playerAmount
        gs.players[x].addBet(bet)
        player_msg = Message("p" + str(x) + "_cards", gs.players[x].hand)
        print(player_msg.id)
        msg.append(player_msg)
    return msg

"""
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
"""

#takes in the player and deck as args, returns the value of player's hand    
def playerTurn(player, deck, numPlayers, gui_to_bj_queue, bj_to_gui_queue):
    move = ''
    bet = player.totalBet
    player_not_done = True
    double = False
    print("player " + str(player.pos) + " turn")
    while player_not_done:  #player move loop
        total = checkValue(player.hand)
        player.showHand()
        print("Total value: {}".format(total))

        time.sleep(.5)

        if total > 21:
            print("Bust!")
            # switch to next player
            if player.pos != int(numPlayers):
                bj_msg = Message("switch", player.pos)
                bj_to_gui_queue.put(bj_msg)
            player_not_done = False
        elif total == 21:
            print("21!")
            if player.pos != int(numPlayers):
                bj_msg = Message("switch", player.pos)
                bj_to_gui_queue.put(bj_msg)
            player_not_done = False
        elif double:
            if player.pos != int(numPlayers):
                bj_msg = Message("switch", player.pos)
                bj_to_gui_queue.put(bj_msg)
            player_not_done = False
        else:
            print("Do you want to hit, stand, or double?")
            waiting_for_msg = True
            while waiting_for_msg:
                msg = gui_to_bj_queue.get()

                # if msg is stand
                if msg.id == "stand":
                    print("received stand msg from GUI")
                    waiting_for_msg = False
                    # tell GUI to continue if not last player
                    print("player.pos: ", player.pos, ", numPlayers: ", numPlayers)
                    if player.pos != int(numPlayers):
                        print("entered if switch...")
                        bj_msg = Message("switch", player.pos)
                        bj_to_gui_queue.put(bj_msg)
                    player_not_done = False
                # if msg is hit
                elif msg.id == "hit":
                    waiting_for_msg = False

                    player.draw(deck)
                    bj_msg = Message("p" + str(player.pos) + "_cards", player.hand)
                    bj_to_gui_queue.put(bj_msg)

                    # player continues move if under 21
                    if total < 21:
                        bj_msg = Message("continue", None)
                        bj_to_gui_queue.put(bj_msg)
                # if msg is double
                elif msg.id == "double":
                    print("BJ entered double")
                    waiting_for_msg = False
                    new_bet = bet*2
                    # not sufficient funds to double
                    if new_bet > int(player.wallet):
                        print("BJ entered new bet > wallet")
                        # TODO: add message to GUI
                        bj_msg = Message("p" + str(player.pos) + "_broke", None)
                        bj_to_gui_queue.put(bj_msg)
                    else:
                        # sufficient funds, draw a card, send to GUI
                        player.addBet(bet)
                        player.draw(deck)
                        bj_msg = Message("p" + str(player.pos) + "_cards", [player.hand, new_bet])
                        bj_to_gui_queue.put(bj_msg)
                        double = True

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
        time.sleep(1)
    return total


"""
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
"""


#takes a player's hand; returns value
def checkValue(hand):
    val = 0
    #sort and add Aces last so choose between 1/11 values
    for card in hand:
        if card.rank == "J":
            card.rank = 11
        elif card.rank == "Q":
            card.rank = 12
        elif card.rank == "K":
            card.rank = 13
        elif card.rank == "A":
            card.rank = 1
    hand.sort(key=lambda x: int(float(x.rank)), reverse=True)
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
    return "{}".format(totals) # testing

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
