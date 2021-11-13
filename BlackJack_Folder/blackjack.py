from gameState import gameState
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from jackblack_homepage import Ui_MainWindow

# change this file to interact with GUI
def main():
    gs = gameState(1)
    while(1):
        totals = []
        # need to figure out ui
        gs.setPlayers((int)(input(Ui_MainWindow.ui.gameModeSelect1ComboBox.currentText())))
        gs.resetHands()
        gs.deck.build()
        gs.deck.shuffle()
        gs.dealCards(2)

        totals.append(0)
        for x in range(1, gs.numPlay):
            totals.append(playerTurn(gs.players[x], gs.deck))
        totals[0] = dealerTurn(gs.players[0], gs.deck)
        score(gs.players, totals)

        gs.showWallets()

        play_again = input("Play again (y/n)?\n").lower()
        if play_again == "y":
            continue
        elif play_again == "n":
            quit() #temporary, should go to some sort of splash s
        else:
            print("\n Invalid answer, quitting.")
            quit() #same as above
    
def playerTurn(player, deck):
    move = ''
    bet = (int) (input("How much do you want to bet? Current wallet = {}\n".format(player.wallet)))
    player.addBet(bet) #handle invalid inputs (if bet > wallet, if no number is given <-- this one shouldnt be a problem when GUI is in place)
    while move != 's':
        total = checkValue(player.hand)
        player.showHand()
        print("Total value: {}".format(total))
        if total > 21:
            print("Bust!")
            break
        elif total == 21:
            print("21!")
            break
        else:
            move = input("Do you want to hit or stand (h/s)?").lower()
            if move == 'h':
                player.draw(deck, 1)
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
            elif totals[x] == 21:
                settleBet(players[x], 0)
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

if __name__ == "__main__":
    main()