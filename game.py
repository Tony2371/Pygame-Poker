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
player_surface = pygame.Surface(((128//3*2+gap*3)*2, 250))
hand_card_1 = pygame.transform.scale(pygame.image.load('deck_images/14s.jpg'), (128//3, 178//3))
hand_card_2 = pygame.transform.scale(pygame.image.load('deck_images/14h.jpg'), (128//3, 178//3))

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
            for card in x.hand:
                card.showing = True
    # Bet blinds

    # ---------- GUI block ----------
    for player in players_in_game:
        window.blit(player_surface, (gap, gap))
        pygame.draw.rect(player_surface, (255, 255, 255), player_surface.get_rect(), 3)
        player_surface.blit(hand_card_1, (gap, gap))
        player_surface.blit(hand_card_2, (gap * 2 + 128 // 3, gap))

        f1 = pygame.font.Font(None, 23)
        line_1 = f1.render(str(player), 0, (255, 255, 255))
        line_2 = f1.render("Chips amount: {0}".format(player.chip_amount), 0, (255, 255, 255))
        line_3 = f1.render("Bet N chips to continue!", 0, (255, 255, 255))

        player_surface.blit(line_1, (gap, gap * 2 + 178 // 3))
        player_surface.blit(line_2, (gap, gap * 4 + 178 // 3))
        player_surface.blit(line_3, (gap, gap * 6 + 178 // 3))

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(30)

pygame.quit()
