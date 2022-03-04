from gameState import gameState
import multiprocessing as mp
import blackjack_globals

from blackjack_globals import Message


def blackjack_process(gui_to_bj_queue, bj_to_gui_queue):
    gameMode = " "
    userInput = 1200 # need to update this in the start_game
    gs = gameState(1, gameMode, userInput)
    #gs.deck.build() #testing, unneeded?
    totals = []

    #count = 0

    # want to do this loop again for each round; change "done" variable?
    done_game = False
    done_round = False
    rounds = 0
    start_var = False
    while not done_game:

        print("start game loop")

        if not start_var:
            msg = gui_to_bj_queue.get() # stuck here
            print("Message ID:" + msg.id)

        if msg.id == "game_start" and rounds == 0:
            start_var = True
            rounds = rounds + 1
            numPlayers = msg.content[0]
            playerWallets = msg.content[1]
            bet = msg.content[2]
            gameMode = msg.content[3]
            userInput = msg.content[4]
        
            msg0, msg1 = start_game(gs, numPlayers, playerWallets, bet, gameMode, userInput)
            gs.deck.build() #testing
            gs.deck.shuffle() #testing
            bj_to_gui_queue.put(msg0)
            bj_to_gui_queue.put(msg1)
            gs.dealCards(2)
            #playerTurn(gs.players[1], gs.deck)
        done_round = False

        while not done_round and start_var:
            # maybe put this line outside this while loop?
            # TODO: after last player finishes their turn, need to clear screen, remove their cards, and give them new cards
            
            print("start round loop") #debug

            #gs.dealCards(2)
            
            playerTurn(gs.players[1], gs.deck)
            msg = gui_to_bj_queue.get()
            print("Message ID: " + msg.id)

            """
            msg = gui_to_bj_queue.get()
            if msg.id == "game_start" and rounds == 0:
                rounds = rounds + 1
                numPlayers = msg.content[0]
                playerWallets = msg.content[1]
                bet = msg.content[2]
                gameMode = msg.content[3]
                userInput = msg.content[4]
            
                msg0, msg1 = start_game(gs, numPlayers, playerWallets, bet, gameMode, userInput)
                gs.deck.build() #testing
                gs.deck.shuffle() #testing
                bj_to_gui_queue.put(msg0)
                bj_to_gui_queue.put(msg1)
                playerTurn(gs.players[1], gs.deck)
            """
            if msg.id == "stand":
                dealerTurn(gs.players[0], gs.deck)
                msg0 = Message("dealer_cards", gs.players[0].hand)
                bj_to_gui_queue.put(msg0)
                #print("Player 1's total: ", checkValue(gs.players[1].hand))

                totals.append(0)
                totals.append(playerTurn(gs.players[1], gs.deck))
                totals[0] = dealerTurn(gs.players[0], gs.deck)
                score(gs.players, totals)
                gs.showWallets()

                msg2 = Message("wallet", gs.players[1].wallet)
                bj_to_gui_queue.put(msg2)
                done_round = True
                rounds = rounds + 1
                # after each round is done, want to clear GUI (tell GUI round_ends) and deal out cards for new round

                # temporary: check player 1's wallet to userInput (winningAmount)
                if gs.players[1].wallet >= gs.userInput:
                    done_game = True
                """
                if rounds == 3:
                    done_game = True
                """
                #count += 1
            elif msg.id == "hit":
                gs.players[1].draw(gs.deck, 1)

                if checkValue(gs.players[1].hand) >= 21:
                    totals.append(0)
                    totals.append(playerTurn(gs.players[1], gs.deck))
                    totals[0] = dealerTurn(gs.players[0], gs.deck)
                    score(gs.players, totals)
                    gs.showWallets()
                    msg2 = Message("wallet", gs.players[1].wallet)
                    bj_to_gui_queue.put(msg2)
                    done_round = True
                    rounds = rounds + 1

                    # temporary: check player 1's wallet to userInput (winningAmount)
                    if gs.players[1].wallet >= gs.userInput:
                        done_game = True
                    """
                    if rounds == 3:
                        done_game = True
                    """
                else:
                    msg1 = Message("player_cards", gs.players[1].hand)
                    bj_to_gui_queue.put(msg1)
                    playerTurn(gs.players[1], gs.deck)
                #done = True
                #count += 1
            elif msg.id == "double":
                # only adding original bet, since original bet was already included
                gs.players[1].draw(gs.deck, 1)
                msg1 = Message("player_cards", gs.players[1].hand)
                bj_to_gui_queue.put(msg1)
                playerTurn(gs.players[1], gs.deck)

                bet = msg.content
                gs.players[1].addBet(bet)
                double = bet * 2

                totals.append(0)
                totals.append(playerTurn(gs.players[1], gs.deck))
                totals[0] = dealerTurn(gs.players[0], gs.deck)
                score(gs.players, totals)
                gs.showWallets()

                msg2 = Message("wallet", gs.players[1].wallet)
                bj_to_gui_queue.put(msg2)

                msg3 = Message("doubled", double)
                bj_to_gui_queue.put(msg3)

                done_round = True
                rounds = rounds + 1

                # temporary: check player 1's wallet to userInput (winningAmount)
                if gs.players[1].wallet >= gs.userInput:
                    done_game = True
                """
                if rounds == 3: # FIX THIS
                    done_game = True
                """
            # here, want to set round to be done and deal out new cards(?)
            elif msg.id == "round_ends":
                pass
            else:
                pass

        print("move done") #debug

        # reset hand, deal 2 cards per player, tell GUI round ended
        if start_var and done_round:
            #done_round = False
            print("done_round now false") #debug
            gs.resetHands()#test
            gs.dealCards(2)
            msg0 = Message("done_round", None)
            bj_to_gui_queue.put(msg0)
            msg1 = Message("player_cards", gs.players[1].hand)
            bj_to_gui_queue.put(msg1)
            playerTurn(gs.players[1], gs.deck)
            msg2 = Message("dealer_cards", gs.players[0].hand)
            bj_to_gui_queue.put(msg2)

        print("round loop end") #debug
        print(f"done_round:{done_round} start_var:{start_var}")

    print("game loop end") #debug
    msg0 = Message("GAME OVER!", None)
    bj_to_gui_queue.put(msg0)

# check game mode; ex. if game mode = # games, keep playing until number of games met

    """
    # play_again = input("Play again (y/n)?\n").lower()
    play_again = blackjack_globals.readBjQueue
    if play_again == "y":
        playerWallets = gs.getWallets()
        #GUI input for numPlayers, bet
        start_game(numPlayers, playerWallets, bet)
    elif play_again == "n":
        quit() #temporary, should go back to menu
    else:
        print("\n Invalid answer, quitting.")
        quit() #same as above
    """

# initializing the start of a game
def start_game(gs, numPlayers, playerAmount, bet, gameMode, userInput):
    gs.setPlayers(numPlayers)

    for x in gs.players:
        x.wallet = playerAmount

    gs.resetHands()
    #gs.deck.build()
    #gs.deck.shuffle()
    #gs.dealCards(2)

    # temporary for one player; need to change for multiple players
    gs.players[1].addBet(bet)

    msg0 = Message("dealer_cards", gs.players[0].hand)
    msg1 = Message("player_cards", gs.players[1].hand)

    return msg0, msg1

def playerTurn(player, deck):
    total = checkValue(player.hand)
    player.showHand()
    print("Total value: {}".format(total))

    if total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")
    else:
        print(total)
    return total

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

#system pays out 2 to 1
def settleBet(player, res):
    if res == 1:
        player.wallet += player.totalBet * 2
    elif res == 0:
        player.wallet += player.totalBet
    #if player loses, bet is just reset
    player.resetBet()

"""
if __name__ == "__main__":
    main()
"""