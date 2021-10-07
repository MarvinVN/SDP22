from gameState import *

def main():
    totals = []
    gs = gameState((int)(input("How many people are playing?")))
    gs.dealCards(2)

    for x in range(1, gs.numPlay):
        totals[x] = playerTurn(gs.players[x], gs.deck)
    totals[0] = dealerTurn(gs.players[0], gs.deck)

def playerTurn(player, deck):
    while move != 's':
        total = checkValue(player.hand)
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
        if total >= 17:
            break
        else:
            player.draw(deck, 1)
    return total

def checkValue(hand):
    val = 0
    for x in hand:
        if x.rank in ['K', 'Q', 'J']:
            val += 10
        elif x == 'A':
            if val >= 11:
                val += 1
            else:
                val += 11
        else:
            val += x.rank
    return val

def score(players, totals):
    return 0