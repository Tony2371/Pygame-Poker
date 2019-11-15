import pygame
from poker_main import Player, StandardDeck, StandardBoard
pygame.init()

deck = StandardDeck()
board = StandardBoard()
player_1 = Player("One")
player_2 = Player("Two")
player_3 = Player("Three")
player_4 = Player("Four")

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Texas Hold'em")
clock = pygame.time.Clock()
suit_dic = {"\u2660": "s", "\u2665": "h", "\u2666": "d", "\u2663": "c"}

running = True

# Game variables
players_in_game = [player_1, player_2,player_3, player_4]
bb_list = [20, 50, 100, 200, 400, 800]
bb = bb_list[0]

# Draw variables
while running:
	# ---------- Game logic block ----------
	# Shuffle deck
	if not deck.shuffled:
		deck.shuffle()

	# Deal cards to players
	if len(player_1.hand) < 2:
		for x in players_in_game:
			x.hand.append(deck.pop(0))
			x.hand.append(deck.pop(0))
		for x in players_in_game:
			#if x == player_1:
				for card in x.hand:
					card.showing = True
	# Bet blinds
	bb_list = [20,50,100,200,400,800]
	bb = bb_list[0]	
	if board.bank < bb+bb//2:
		board.blind_bet(players_in_game, bb)

	#Player decisions
	bets_not_done = True
	if len(set([x.current_bet for x in players_in_game])) != 1:
		for player in players_in_game:
			if player.ingame:
				print("{0} need to bet {1} chips to continue".format(player.name,max([x.current_bet for x in players_in_game])-player.current_bet))
				player.decision(input("Decision:"),players_in_game,board)
		if len(set([player.current_bet for player in players_in_game if player.ingame])) == 1:
			bets_not_done = False



	# Deal Flop
	if len(board) < 3 and len(set([player.current_bet for player in players_in_game if player.ingame])) == 1:
		board.append(deck.pop(0))
		board.append(deck.pop(0))
		board.append(deck.pop(0))
		for x in board:
			x.showing = True
		board.street = "flop"
		for x in players_in_game:
			x.current_bet = 0

	#Player decisions

	#Deal Turn

	#Player decisions

	#Deal River

	#Player decisions

	#Combination comparison and winner selection

	#Reset game state for new round

	for player in players_in_game:
		if player.ingame:
			player.evaluate(board)



	# ---------- GUI block ----------
	player_1.draw_player_surface(window,(10,10),players_in_game)
	player_2.draw_player_surface(window,(64.8+114,10), players_in_game)
	player_3.draw_player_surface(window,(64.8*2+114*2,10), players_in_game)
	player_4.draw_player_surface(window,(64.8*3+114*3,10), players_in_game)


	board.draw_board_surface(window)


	for event in pygame.event.get():
		if event.type == pygame.QUIT or len(board) > 5:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				board.append(deck.pop(0))
				for x in players_in_game:
					x.evaluate(board)
				for x in board:
					x.showing = True

	pygame.display.update()

	clock.tick(15)
	print(set([x.current_bet for x in players_in_game]))
pygame.quit()
