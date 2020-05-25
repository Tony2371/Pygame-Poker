'''
TO DO LIST:
- Side pots mechanic

KNOWN BUGS:
- Fixed all bugs for now

SMALL ISSUES:
- Four of a kind doesnt have kicker because it doesnt need
- Small chip loss due to rounding in case of pot split
'''

from poker_main import Player, StandardDeck, StandardBoard
from random import randint

deck = StandardDeck()
board = StandardBoard()
player_1 = Player("One")
player_2 = Player("Two")
player_3 = Player("Three")
player_4 = Player("Four")
player_5 = Player("Five")
player_6 = Player("Six")
player_7 = Player("Seven")
player_8 = Player("Eight")
player_9 = Player("Nine")

#players_in_game = [player_1,player_2,player_3,player_4,player_5,player_6,player_7,player_8,player_9]
players_in_game = [player_1,player_2,player_3,player_4,player_5,player_6]
running = True

while running:
	for player in players_in_game:
		player.reset()
	board.reset()
	deck.reset()
	if not deck.shuffled:
		deck.shuffle()
	# --------------------------PREFLOP-----------------------------------
	players_in_game.append(players_in_game.pop(0))
	board.blind_bet(players_in_game)

	for player in players_in_game:
		player.hand.append(deck.pop(0))
		player.hand.append(deck.pop(0))

	board.check_bets(players_in_game,board)
	board.check_winner(players_in_game)
	print("Preflop ended!")

	# --------------------------FLOP-----------------------------------
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.append(deck.pop(0))

	print("Board: ",board)

	board.check_bets(players_in_game,board)
	board.check_winner(players_in_game)
	print("Flop ended!")

	# --------------------------TURN-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game,board)
	board.check_winner(players_in_game)
	print("Turn ended!")

	# --------------------------RIVER-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game,board)
	board.check_winner(players_in_game)
	print("River ended!")
	board.game_round += 1
	# --------------------------POSTGAME-----------------------------------
	print("########################################")
	print("Round:",board.game_round)
	print(board)
	print("BB:",board.blinds_list[0])
	for player in players_in_game:
		print(player,"|",player.chip_amount,"|",player.hand,"|",player.combination)

	if sum([player.chip_amount for player in players_in_game]) != 1500*6:
		print("ERROR!!!")
		running = False

	for player in players_in_game:
		if player.chip_amount <= 0:
			players_in_game.remove(player)
			print(player, "eliminated!")

	if len(players_in_game) == 1:
		print(players_in_game[0], "won 'em all!")
		running = False
