'''
TO DO LIST:
- Raise is possbile for minimum amount equal to blind
- Bank split situation
- All-in bank split

KNOWN BUGS:
- no bugs known for now

SMALL ISSUES:
- Four of a kind doesnt have kicker because it doesnt need
- If (probably not only) "straight", combination shows kickers
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

	board.check_bets(players_in_game)
	if board.check_winner(players_in_game):
		break
	print("Preflop ended!")

	# --------------------------FLOP-----------------------------------
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.append(deck.pop(0))

	print("Board: ",board)

	board.check_bets(players_in_game)
	board.check_winner(players_in_game)
	print("Flop ended!")

	# --------------------------TURN-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game)
	board.check_winner(players_in_game)
	print("Turn ended!")

	# --------------------------RIVER-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game)
	board.check_winner(players_in_game)
	print("River ended!")

	print("########################################")
	print("Round:",board.game_round)
	print("Blinds:",board.blinds_list[0],board.blinds_list[0]//2)
	print("Blinds:",)
	print(board)
	for player in players_in_game:
		print(player,"|",player.chip_amount,"|",player.hand,"|",player.combination)

	for player in players_in_game:
		if player.chip_amount <= 0:
			players_in_game.remove(player)
			print(player, "eliminated!")

	#xyz = input("Continue")

	if len(players_in_game) == 1:
		print(players_in_game[0], "won 'em all!")
		running = False
