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
    #gs.deck.build() #testing, unneeded?

    #count = 0

    # want to do this loop again for each round; change "done" variable?
    done_game = False
    done_round = False
    rounds = 0
    num_wins = 0
    game_duration = 0 # keep track of length of game
    start_var = False
    bust = False
    bj = False
    round_score = []
    while not done_game:
        totals = []
        bust = False
        bj = False
        print("start game loop")

        if not start_var:
            msg = gui_to_bj_queue.get() # stuck here
            print("Message ID:" + msg.id)

        if msg.id == "game_start":
            start_var = True
            #rounds = rounds + 1
            numPlayers = msg.content[0]
            playerWallets = msg.content[1]
            bet = msg.content[2]
            gameMode = msg.content[3]
            gs.userInput = msg.content[4]
            print("Game Start User Input:" + str(gs.userInput))
        
            player_msg = start_game(gs, numPlayers, playerWallets, bet, gameMode, gs.userInput)
            #gs.deck.build() #testing
            #gs.deck.shuffle() #testing

            """
            # adding dealer shuffle
            dealer.shuffle()

            sleep(2)

            #gs.dealCards(2)
            # dealing cards to dealer and player 1
            dealer.p1()
            gs.players[0].draw(gs.deck, 1)
            dealer.p2()
            gs.players[1].draw(gs.deck, 1)
            dealer.p1()
            gs.players[0].draw(gs.deck, 1)
            dealer.p2()
            gs.players[1].draw(gs.deck, 1)

            """
            for x in player_msg:
                bj_to_gui_queue.put(x)
                print("Put in player message: " + str(x.id))

            #playerTurn(gs.players[1], gs.deck)
        done_round = False

        while not done_round and start_var:
            # maybe put this line outside this while loop?
            # TODO: after last player finishes their turn, need to clear screen, remove their cards, and give them new cards
            
            print("start round loop") #debug

            #gs.dealCards(2)
            for x in range(gs.numPlay):
                playerTurn(gs.players[x+1], gs.deck)
                # not receiving message?
                msg = gui_to_bj_queue.get()
                print("Message ID: " + msg.id)

                if msg.id == "stand":
                    # need to change this for after whoever plays last
                    dealerTurn(gs.players[0], gs.deck)
                    msg0 = Message("dealer_cards", gs.players[0].hand)
                    bj_to_gui_queue.put(msg0)
                    #print("Player 1's total: ", checkValue(gs.players[1].hand))

                    totals.append(0)
                    totals.append(playerTurn(gs.players[1], gs.deck))
                    totals[0] = dealerTurn(gs.players[0], gs.deck)
                
                    round_score = score(gs.players, totals)
                    gs.showWallets()
                

                    msg2 = Message("wallet", gs.players[1].wallet)
                    bj_to_gui_queue.put(msg2)
                    """
                    score(gs.players, totals)
                    gs.showWallets()
                    """

                    done_round = True
                    rounds = rounds + 1
                    t2 = time.time()
                    total_time = (t2 - t1)
                    # check value of gameMode
                    #print("gameMode is: " + str(gs.gameMode))

                    if checkValue(gs.players[1].hand) > checkValue(gs.players[0].hand):
                        num_wins = num_wins + 1
                        print("Num Wins: " + str(num_wins))
                    elif checkValue(gs.players[0].hand) > 21:
                        num_wins = num_wins + 1
                    else:
                        pass                

                    #print("gs.players[1].wallet: " + str(gs.players[1].wallet))
                    #print("gs.userInput: " + str(gs.userInput))
                    # game end states (testing); none of these are printing
                    if gs.gameMode == "Winning Amount":
                        if gs.players[1].wallet >= gs.userInput:
                            done_game = True
                            print("Winning Amount Game Over")
                    elif gs.gameMode == "Number of Wins":
                        if num_wins == gs.userInput:
                            done_game = True
                            print("Number of Wins Game Over")
                    elif gs.gameMode == "Total Games":
                        if rounds == gs.userInput:
                            done_game = True
                            print("Total Games Game Over")
                    elif gs.gameMode == "Duration":
                        if total_time >= gs.userInput:
                            done_game = True
                            print("Duration Game Over")
                    else:
                        print("nothing worked")

                elif msg.id == "hit":
                    gs.players[1].draw(gs.deck, 1)
                    #dealer.p2()

                    if checkValue(gs.players[1].hand) > 21:
                    
                        totals.append(0)
                        totals.append(playerTurn(gs.players[1], gs.deck))
                        totals[0] = dealerTurn(gs.players[0], gs.deck)
                        round_score = score(gs.players, totals)
                        gs.showWallets()
                        msg2 = Message("wallet", gs.players[1].wallet)
                        bj_to_gui_queue.put(msg2)
                    
                        done_round = True
                        rounds = rounds + 1
                        t2 = time.time()
                        total_time = (t2 - t1)
                        # check value of gameMode
                        print("gameMode is: " + str(gs.gameMode))

                        # game end states (testing); none of these are printing
                        if gs.gameMode == "Winning Amount":
                            if gs.players[1].wallet >= gs.userInput:
                                done_game = True
                                print("Winning Amount Game Over")
                        elif gs.gameMode == "Number of Wins":
                            print("entered num wins statement")
                            if num_wins == gs.userInput:
                                done_game = True
                                print("Number of Wins Game Over")
                        elif gs.gameMode == "Total Games":
                            if rounds == gs.userInput:
                                done_game = True
                                print("Total Games Game Over")
                        elif gs.gameMode == "Duration":
                            if total_time >= gs.userInput:
                                done_game = True
                                print("Duration Game Over")
                        else:
                            print("nothing worked")        

                    else:
                        msg1 = Message("player_cards", gs.players[1].hand)
                        bj_to_gui_queue.put(msg1)
                        playerTurn(gs.players[1], gs.deck)
                    #done = True
                    #count += 1
                elif msg.id == "double":
                    # only adding original bet, since original bet was already included
                    totals.append(0)
                    bet = msg.content[0][0]
                    check_player = msg.content[1]
                    if check_player == "p1":
                        gs.players[1].draw(gs.deck, 1)
                        msg1 = Message("p1_cards", gs.players[1].hand)
                        bj_to_gui_queue.put(msg1)

                        playerTurn(gs.players[1], gs.deck)
                        bet = msg.content[0][1]
                        gs.players[1].addBet(bet)
                        totals.append(playerTurn(gs.players[1], gs.deck))
                    elif check_player == "p2":
                        gs.players[2].draw(gs.deck, 1)
                        msg1 = Message("p2_cards", gs.players[2].hand)
                        bj_to_gui_queue.put(msg1)

                        playerTurn(gs.players[2], gs.deck)
                        bet = msg.content[0][2]
                        gs.players[2].addBet(bet)
                        totals.append(playerTurn(gs.players[2], gs.deck))
                    elif check_player == "p3":
                        gs.players[3].draw(gs.deck, 1)
                        msg1 = Message("p3_cards", gs.players[3].hand)
                        bj_to_gui_queue.put(msg1)

                        playerTurn(gs.players[3], gs.deck)
                        bet = msg.content[0][3]
                        gs.players[3].addBet(bet)
                        totals.append(playerTurn(gs.players[3], gs.deck))
                    elif check_player == "p4":
                        gs.players[4].draw(gs.deck, 1)
                        msg1 = Message("p4_cards", gs.players[4].hand)
                        bj_to_gui_queue.put(msg1)

                        playerTurn(gs.players[4], gs.deck)
                        bet = msg.content[0][4]
                        gs.players[4].addBet(bet)
                        totals.append(playerTurn(gs.players[4], gs.deck))
                    else:
                        print("None of the players doubled!")
                    
                    #dealer.p2()
                    
                    double = bet * 2

                    totals[0] = dealerTurn(gs.players[0], gs.deck)
                    round_score = score(gs.players, totals)
                    gs.showWallets()

                    msg2 = Message("wallet", gs.players[1].wallet)
                    bj_to_gui_queue.put(msg2)

                    msg3 = Message("doubled", double)
                    bj_to_gui_queue.put(msg3)

                    done_round = True
                    rounds = rounds + 1
                    t2 = time.time()
                    total_time = (t2 - t1)
                    # check value of gameMode
                    print("gameMode is: " + str(gs.gameMode))

                    if checkValue(gs.players[1].hand) <= 21:
                        if checkValue(gs.players[1].hand) > checkValue(gs.players[0].hand):
                            num_wins = num_wins + 1
                            #print("Num Wins: " + str(num_wins))
                        elif checkValue(gs.players[0].hand) > 21:
                            num_wins = num_wins + 1
                        else:
                            pass
                    else:
                        print("Num Wins did not change.") # not printing

                    # game end states (testing)
                    # need to change this for multiplayers
                    if gs.gameMode == "Winning Amount":
                        if gs.players[1].wallet >= gs.userInput:
                            done_game = True
                            print("Winning Amount Game Over")
                    elif gs.gameMode == "Number of Wins":
                        if num_wins == gs.userInput:
                            done_game = True
                            print("Number of Wins Game Over")
                    elif gs.gameMode == "Total Games":
                        if rounds == gs.userInput:
                            done_game = True
                            print("Total Games Game Over")
                    elif gs.gameMode == "Duration":
                        if total_time >= gs.userInput:
                            done_game = True
                            print("Duration Game Over")
                    else:
                        print("nothing worked")    
                else:
                    pass

        print("move done") #debug
        print("Number of Rounds:" + str(rounds))
        print("Number of Wins:" + str(num_wins))
        print("Duration of Time (sec):" + str(total_time))
        print("User Input:" + str(gs.userInput))

        # reset hand, deal 2 cards per player, tell GUI round ended
        if start_var and done_round:
            #done_round = False
            print("done_round now false") #debug
            
            if checkValue(gs.players[1].hand) > 21:
                bust = True
            
            if checkValue(gs.players[1].hand) == 21:
                bj = True
            msg0 = Message("done_round", [gs.players[0].hand,gs.players[1].hand, round_score, gs.getWallets(), bust, bj])
            bj_to_gui_queue.put(msg0)

            if done_game:
                # change True to (True/False) depending on which player wins
                msg0 = Message("GAME OVER!", [num_wins, True])
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
            """
            dealer.p1()
            gs.players[0].draw(gs.deck, 1)
            dealer.p2()
            gs.players[1].draw(gs.deck, 1)
            dealer.p1()
            gs.players[0].draw(gs.deck, 1)
            dealer.p2()
            gs.players[1].draw(gs.deck, 1)
            """


            # temporary for one player:
            gs.players[1].resetBet()
            gs.players[1].addBet(bet)

            msg1 = Message("player_cards", gs.players[1].hand)
            bj_to_gui_queue.put(msg1)
            playerTurn(gs.players[1], gs.deck)
            msg2 = Message("dealer_cards", gs.players[0].hand)
            bj_to_gui_queue.put(msg2)

        print("----------------------------------------------------") #debug
        #print(f"done_round:{done_round} start_var:{start_var} done_game:{done_game}")

    print("game loop end") #debug
    #msg0 = Message("GAME OVER!", None)
    #bj_to_gui_queue.put(msg0)

# initializing the start of a game
def start_game(gs, numPlayers, playerAmount, bet, gameMode, userInput):
    # making msg list for each player
    msg = []
    gs.setPlayers(numPlayers)
    print("NumPlayers = " + str(numPlayers))
    gs.userInput = userInput
    gs.gameMode = gameMode

    gs.resetHands()
    gs.deck.build()
    gs.deck.shuffle()
    gs.dealCards(2)

    for x in range(gs.numPlay):
        # this does not include dealer
        gs.players[x].wallet = playerAmount
        gs.players[x].addBet(bet)
        player_msg = Message("p" + str(x) + "_cards", gs.players[x].hand)
        print(player_msg.id)
        msg.append(player_msg)

    #gs.deck.build()
    #gs.deck.shuffle()
    #gs.dealCards(2)

   # msg0 = Message("dealer_cards", gs.players[0].hand)
   # msg1 = Message("player_cards", gs.players[1].hand)

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

def playerTurn(player, deck):
    total = checkValue(player.hand)
    #player.showHand() this prints hand
    #print("Player value: {}".format(total))

    if total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")
    else:
        print("Player: {}" .format(total))
    return total

def dealerTurn(player, deck):
    total = 0
    while total < 17:
        total = checkValue(player.hand)
        #player.showHand()
        print("Dealer: {}".format(total))
        if total >= 17:
            break
        else:
            player.draw(deck, 1)
            dealer.p1()
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
    #if player loses, bet is just reset
    #player.resetBet()

"""
if __name__ == "__main__":
    main()
"""