from gameState import gameState
from game import Deck
import dealer
import multiprocessing as mp
import blackjack_globals
import time
from time import sleep

from blackjack_globals import Message

t1 = time.time()
t2 = time.time()

def blackjack_process(gui_to_bj_queue, bj_to_gui_queue):
    gameMode = " "
    userInput = 0 # need to update this in the start_game
    gs = gameState(1, gameMode, userInput)

    done_game = False
    done_round = False
    done_player_round = False
    rounds = 0
    wins_list = [0,0,0,0,0]
    winner = 0
    game_duration = 0 # keep track of length of game
    start_var = False
    round_score = []
    numPlayers = ""
    while not done_game:
        totals = []
        print("start game loop")

        if not start_var:
            msg = gui_to_bj_queue.get() # stuck here
            print("Message ID:" + msg.id)

        if msg.id == "game_start":
            start_var = True
            numPlayers = msg.content[0]
            playerWallets = msg.content[1]
            bet = msg.content[2]
            gameMode = msg.content[3]
            gs.userInput = msg.content[4]
            for x in range(int(numPlayers)+1):
                totals.append(0)
            print("Game Start User Input:" + str(gs.userInput))
        
            player_msg = start_game(gs, numPlayers, playerWallets, bet, gameMode, gs.userInput)

            for x in player_msg:
                print("before cards: ", x.id, x.content)
                bj_to_gui_queue.put(x)
                print("Put in player message: " + str(x.id))
                print("Put in player cards: " + str(x.content))

        done_round = False # each ROUND is after all players haven taken their turn

        for x in range(1, gs.numPlay):            
            print("start player loop") #debug
            done_player_round = False

            while not done_player_round and start_var:
                playerTurn(x, gs.players[x], gs.deck)
                msg = gui_to_bj_queue.get()
                print("Message ID: " + msg.id)

                if msg.id == "stand":
                    totals[x] = playerTurn(x, gs.players[x], gs.deck)

                    if str(x) != numPlayers:
                        print("x is: " + str(x) + ", numPlayers is: " + numPlayers)
                        msg2 = Message("continue", None)
                        bj_to_gui_queue.put(msg2)
                        print("sending CONTINUE msg to GUI...")
                    done_player_round = True

                elif msg.id == "hit":
                    gs.players[x].draw(gs.deck, 1)
                    totals[x] = playerTurn(x, gs.players[x], gs.deck)
                    msg1 = Message("p" + str(x) + "_cards", gs.players[x].hand)
                    bj_to_gui_queue.put(msg1)

                    if str(x) != numPlayers:
                        msg2 = Message("continue", None)
                        bj_to_gui_queue.put(msg2)
                    elif str(x) == numPlayers and (checkValue(gs.players[x].hand) <= 21):
                        msg2 = Message("continue", None)
                        bj_to_gui_queue.put(msg2)
                    else:
                        pass

                    if checkValue(gs.players[x].hand) > 21:
                        done_player_round = True

                elif msg.id == "double":
                    # only adding original bet, since original bet was already included
                    bet = msg.content[x]
                    gs.players[x].draw(gs.deck, 1)
                    msg1 = Message("p" + str(x) + "_cards", gs.players[x].hand)
                    bj_to_gui_queue.put(msg1)
                    print("Msg double ID: " + str(msg1.id) + ", Contents: " + str(msg1.content))

                    gs.players[x].addBet(bet)
                    totals[x] = playerTurn(x, gs.players[x], gs.deck)

                    msg3 = Message("doubled", double)
                    bj_to_gui_queue.put(msg3)
                    
                    if str(x) != numPlayers:
                        msg2 = Message("continue", None)
                        bj_to_gui_queue.put(msg2)
                    done_player_round = True

                else:
                    pass
        print("finished one full round of players...")
        done_round = True # this happens after all players have gone
        # Dealer goes after all players go
        dealerTurn(gs.players[0], gs.deck)
        totals[0] = dealerTurn(gs.players[0], gs.deck)
        round_score = score(gs.players, totals)
        gs.showWallets()
        msg0 = Message("done_round", [gs.players[0].hand, round_score, gs.getWallets()])
        bj_to_gui_queue.put(msg0)
        print("sending DONE_ROUND msg to GUI...")

        """
        # wait for a message to confirm round successfully over before starting new round
        while(1):
            complete_round = gui_to_bj_queue.get()
            if complete_round.id == "complete_round":
                break
        """

        # reset hand, deal 2 cards per player, tell GUI round ended
        if start_var and done_round:
            print("done round, checking game states...")
            t2 = time.time()
            total_time = (t2 - t1)

            rounds = rounds + 1

            for x in range(1, gs.numPlay):
                if checkValue(gs.players[x].hand) > checkValue(gs.players[0].hand):
                    wins_list[x] = wins_list[x] + 1
                elif checkValue(gs.players[0].hand) > 21:
                    wins_list[x] = wins_list[x] + 1

                if gs.gameMode == "Winning Amount":
                    if gs.players[x].wallet >= gs.userInput:
                        done_game = True
                        winner = x
                        print("Winning Amount Game Over")
                elif gs.gameMode == "Number of Wins":
                    if wins_list[x] == gs.userInput:
                        done_game = True
                        winner = x
                        print("Number of Wins Game Over")
                elif gs.gameMode == "Total Games":
                    if rounds == gs.userInput:
                        done_game = True
                        winner = x
                        print("Total Games Game Over")
                elif gs.gameMode == "Duration":
                    if total_time >= gs.userInput:
                        done_game = True
                        winner = x
                        print("Duration Game Over")
                else:
                    print("no one won yet...")
            
            if done_game: # send over winner's winning information
                msg0 = Message("GAME OVER!", [winner, True])
                bj_to_gui_queue.put(msg0)
            # check if the deck is empty
            elif not gs.deck.cards:
                print("New set of Deck!")
                gs.deck = Deck()
            elif len(gs.deck.cards) <= 10:
                print("Shuffling deck with 10 cards left!")
                gs.deck = Deck()
            else:
                pass

            gs.resetHands()#test
            gs.dealCards(2)

            for x in range(gs.numPlay):
                gs.players[x].resetBet()
                gs.players[x].addBet(bet)

                msg1 = Message("p" + str(x) + "_cards", gs.players[x].hand)
                bj_to_gui_queue.put(msg1)
                #playerTurn(x, gs.players[x], gs.deck)


        print("----------------------------------------------------") #debug
        #print(f"done_round:{done_round} start_var:{start_var} done_game:{done_game}")

    print("game loop end") #debug

# initializing the start of a game
def start_game(gs, numPlayers, playerAmount, bet, gameMode, userInput):
    # making msg list for each player
    msg = []
    gs.setPlayers(int(numPlayers))
    print("NumPlayers = " + str(numPlayers))
    gs.userInput = userInput
    gs.gameMode = gameMode

    gs.resetHands()
    gs.deck.build()
    gs.deck.shuffle()
    gs.dealCards(2)

    #print(gs.players)
    print("numPlay: " + str(gs.numPlay))
    for x in range(gs.numPlay):
        # this does not include dealer
        gs.players[x].wallet = playerAmount
        gs.players[x].addBet(bet)
        player_msg = Message("p" + str(x) + "_cards", gs.players[x].hand)
        print(player_msg.id)
        msg.append(player_msg)
    return msg

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

def playerTurn(x, player, deck):
    total = checkValue(player.hand)

    if total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")
    else:
        print("Player " + str(x) + ": {}".format(total))
    return total

def dealerTurn(player, deck):
    total = 0
    while total < 17:
        total = checkValue(player.hand)
        print("Dealer: {}".format(total))
        if total >= 17:
            break
        else:
            player.draw(deck, 1)
            #dealer.p1()
    return total

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

#clean up
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
    return "{}".format(totals) # testing

#system pays out 2 to 1
def settleBet(player, res):
    if res == 1:
        player.wallet += player.totalBet * 2
    elif res == 0:
        player.wallet += player.totalBet
