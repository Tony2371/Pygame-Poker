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

comb_names = {
	1:"High Card",
	2:"Pair",
	3:"Two pairs",
	4:"Three of a kind",
	5:"Straight",
	6:"Flush",
	7:"Full house",
	8:"Four of a kind",
	9:"Straight flush"}

deck = StandardDeck()
board = StandardBoard()
player1 = Player("One")
you = Player("You")
player3 = Player("Three")
player4 = Player("Four")

players_in_game = [you, player1]
players_in_round = []
run = True
bb_list = [20,50,100,200,400,800]
bb = bb_list[0]


while run:
	
    board.game_round += 1
    print([x.chip_amount for x in players_in_game])

    if board.game_round%5 == 0:
        bb = bb_list[board.game_round//5]
    players_in_game.append(players_in_game.pop(0))
    board.blind_bet(players_in_game, bb)

    # PreFlop
    deck.shuffle()

    for x in players_in_game:
    	x.hand.append(deck.pop(0))
    	x.hand.append(deck.pop(0))
    	for l in x.hand:
    		l.showing = True

    for x in players_in_game:
    	print(x,x.hand)

    print("Blinds:")
    for x in players_in_game:
    	print(x,x.current_bet)

    for x in players_in_game:
    	if x.current_bet < max([x.current_bet for x in players_in_game]):
    		print("{0} needs to bet {1} to continue".format(x,max([x.current_bet for x in players_in_game])-x.current_bet))

    you.decision(input("Decision:"),players_in_game,board)
    break

	




