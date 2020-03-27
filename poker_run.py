'''
TO DO LIST:
- Low Straight flush combination (SOLVED)
- Kickers
- Second high card for Two pairs and Full House

KNOWN BUGS:
- max([x for x,y in zip(self.val_list,self.count_list) if y == 1])
will be empty sequence if none of y == 1
- Full house error if two sets

GAME STAGES:

'''
from poker_main import Player, StandardDeck, StandardBoard
from random import randint

comb_names = {
	1: "High Card",
	2: "Pair",
	3: "Two pairs",
	4: "Three of a kind",
	5: "Straight",
	6: "Flush",
	7: "Full house",
	8: "Four of a kind",
	9: "Straight flush"}

deck = StandardDeck()
board = StandardBoard()
player_1 = Player("One")


if __name__ == "__main__":
	counter = 0
	while True:
		counter += 1
		deck = StandardDeck()
		board = StandardBoard()
		player_1 = Player("One")
		player_2 = Player("Two")
		deck.shuffle()
		for card in deck:
			card.showing = True


		player_1.hand.append(deck.pop(randint(0,len(deck)-1)))
		player_1.hand.append(deck.pop(randint(0,len(deck)-1)))
		player_2.hand.append(deck.pop(randint(0,len(deck)-1)))
		player_2.hand.append(deck.pop(randint(0,len(deck)-1)))

		board.append(deck.pop(randint(0,len(deck)-1)))
		board.append(deck.pop(randint(0,len(deck)-1)))
		board.append(deck.pop(randint(0,len(deck)-1)))
		board.append(deck.pop(randint(0,len(deck)-1)))
		board.append(deck.pop(randint(0,len(deck)-1)))

		print(counter)
		print(player_1,player_1.hand)
		print(player_2,player_2.hand)
		print(board)

		player_1.evaluate(board)
		player_2.evaluate(board)

		print("------------------------------------------------")
		print(comb_names[player_1.combination[0]], "of", player_1.combination[1], "and", player_1.combination[2])
		print("Kicker:", player_1.kicker[0])
		print(comb_names[player_2.combination[0]], "of", player_2.combination[1], "and", player_2.combination[2])
		print("Kicker:", player_2.kicker[0])
