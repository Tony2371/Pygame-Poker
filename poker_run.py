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
- shuffle deck
- deal cards
- bet blinds
	- reset current_bets
- deal flop
- make bets
	- reset current_bets
- deal turn
- make bets
	- reset current_bets
- deal river
- make bets
	- reset current_bets
- evaluate hands
- determine winner and prize
- reset hands
- reset board
- reset deck
'''
from poker_main import Card, Player, StandardDeck, StandardBoard
from random import randint
from time import sleep

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

players_in_game = [you, player1, player3,player4]
players_in_round = []
run = True
bb_list = [20,50,100,200,400,800]
bb = bb_list[0]

while run:
    board.game_round += 1
    if board.game_round%5 == 0:
        bb = bb_list[board.game_round//5]
    players_in_game.append(players_in_game.pop(0))
    board.blind_bet(players_in_game,bb)

    deck.shuffle()
    board.bank += player4.bet(100)
    for x in players_in_game:
        [x.hand.append(deck.pop(0)) for y in range(2)]
        if x == you:
            for y in x.hand:
                y.showing = True
        print("{0}'s hand: {1} | Current bet: {2}".format(x, x.hand,x.current_bet))


    print("Big blind: {0} | {1}".format(bb, players_in_game[0]))
    print("Small blind: {0} | {1}".format(bb//2, players_in_game[1]))
    print("Current bank:",board.bank)
    print("You need to bet {0} to continue".format(max([x.current_bet for x in players_in_game])-you.current_bet))
    board.bank += you.bet(100)

    for x in players_in_game:
    	if x.current_bet == max([x.current_bet for x in players_in_game]):
    		players_in_round.append(x)
    		x.current_bet = 0
    print(players_in_round, "in game!")
    print("Current bank:",board.bank)

    for x in range(5):
    	board.append(deck.pop(0))

    for x in board:
    	x.showing = True

    print(board)
    you.evaluate(board)
    player4.evaluate(board)

    print(you.combination)
    print(player4.combination)

    if you.combination[0]>player4.combination[0]:
    	print("You win!")
    	you.chip_amount += board.bank
    	board.bank == 0
    else:
    	print("Player4 wins!")
    	player4.chip_amount += board.bank
    	board.bank == 0

    for x in players_in_game:
    	print(x.chip_amount)

    break

	




