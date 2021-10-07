from gameState import *

gs = gameState(1)
print(gs.players[1].getWallet())
print(gs.players[1].getTotalBet())

print("------------------bet 250-----------------------")
gs.players[1].addBet(250)
print(gs.players[1].getWallet())
print(gs.players[1].getTotalBet())

print("------------------go all in-----------------------")
gs.players[1].allIn()
print(gs.players[1].getWallet())
print(gs.players[1].getTotalBet())

print("------------------reset bet, add 500-----------------------")
gs.players[1].addWallet(500)
gs.resetBets()
print(gs.players[1].getWallet())
print(gs.players[1].getTotalBet())