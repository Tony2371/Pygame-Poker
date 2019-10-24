import pygame
from poker_main import Player, StandardDeck, StandardBoard
pygame.init()

deck = StandardDeck()
board = StandardBoard()
player_1 = Player("One")
player_2 = Player("Two")

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Texas Hold'em")
clock = pygame.time.Clock()
suit_dic = {"\u2660": "s", "\u2665": "h", "\u2666": "d", "\u2663": "c"}

running = True

# Game variables
players_in_game = [player_1, player_2]
bb_list = [20, 50, 100, 200, 400, 800]
bb = bb_list[0]

# Draw variables
gap = 10
gap_x = -228*3
hand_card_1 = pygame.transform.scale(pygame.image.load('deck_images/14s.jpg'), (128//3, 178//3))
hand_card_2 = pygame.transform.scale(pygame.image.load('deck_images/14h.jpg'), (128//3, 178//3))
windows_spawned = 0
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
	while board.bank < bb+bb//2:
		board.blind_bet(players_in_game, bb)
	
	while len(board) < 5:
		for x in range(5):
			board.append(deck.pop(0))
		for x in board:
			x.showing = True


	# ---------- GUI block ----------
	while windows_spawned <= 2:
		for player in players_in_game:
			windows_spawned += 1
			gap_x += player.surface.get_width()+45

			player.draw_player_surface(window, gap_x, players_in_game)


	board.draw_board_surface(window)

		
	pygame.display.update()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	clock.tick(15)

pygame.quit()
