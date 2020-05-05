'''
TO DO LIST:
- Kickers for all combinations
- Second high card for Two pairs and Full House
- Bank split situation

KNOWN BUGS:
- max([x for x,y in zip(self.val_list,self.count_list) if y == 1])
will be empty sequence if none of y == 1

SMALL ISSUES:
- Four of a kind doesnt have kicker because it doesnt need
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
	board.blind_bet(players_in_game, board.current_blind)

	for player in players_in_game:
		player.hand.append(deck.pop(0))
		player.hand.append(deck.pop(0))

	board.check_bets(players_in_game, board)
	if board.check_winner(players_in_game,board):
		break
	print("Preflop ended!")

	# --------------------------FLOP-----------------------------------
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.append(deck.pop(0))

	print("Board: ",board)

	board.check_bets(players_in_game, board)
	board.check_winner(players_in_game, board)
	print("Flop ended!")

	# --------------------------TURN-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game, board)
	board.check_winner(players_in_game, board)
	print("Turn ended!")

	# --------------------------RIVER-----------------------------------
	board.append(deck.pop(0))
	print("Board: ",board)

	board.check_bets(players_in_game, board)
	board.check_winner(players_in_game, board)
	print("River ended!")

	print("########################################")
	print(board)
	print("Bank:",board.bank)
	for player in players_in_game:
		print(player,"|",player.chip_amount,"|",player.hand,"|",player.combination)

	for player in players_in_game:
		if player.chip_amount <= 0:
			players_in_game.remove(player)

	for player in players_in_game:
		if player.count_list.count(3) == 6:
			print(player.count_list)
			running = False
