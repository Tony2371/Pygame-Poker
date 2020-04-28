'''
TO DO LIST:
- Kickers
- Second high card for Two pairs and Full House

KNOWN BUGS:
- max([x for x,y in zip(self.val_list,self.count_list) if y == 1])
will be empty sequence if none of y == 1
- Full house error if two sets
-
'''
from poker_main import Player, StandardDeck, StandardBoard
from random import randint

deck = StandardDeck()
board = StandardBoard()
player_1 = Player("One")
player_2 = Player("Two")
player_3 = Player("Three")
player_4 = Player("Four")

players_in_game = [player_1,player_2,player_3,player_4]
game_stages = []

def check_bets(players):
	while True:
		for player in players:
			if player.ingame and not player.answered:
				print(player,", you'd better make a bet!")
				player.decision(input("Decision:"),players_in_game,board)
		if all([player.answered for player in players if player.ingame]):
			break
	print("Bets done!!!")

	for player in players_in_game:
		player.answered = False

while True:
	deck.reset()
	if not deck.shuffled:
		deck.shuffle()

	for player in players_in_game:
		player.hand.append(deck.pop(0))
		player.hand.append(deck.pop(0))
		print("--------",player,"--------")
		print("Cards: ",player.hand)
		print(player.chip_amount)
		print(player.current_bet)
	print("Bank:",board.bank)

	board.blind_bet(players_in_game,100)
	check_bets(players_in_game)
	print("Preflop ended!")

	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	print("Board: ",board)

	check_bets(players_in_game)
	print("Flop ended!")


	break
