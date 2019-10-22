import pygame
from random import randint
pygame.init()

win_width = 800
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("PyGame test")

clock = pygame.time.Clock()
running = True

# Draw variables
gap = 10
player_1_surface = pygame.Surface(((128//3*2+gap*3)*2, 250))
hand_card_1 = pygame.transform.scale(pygame.image.load('deck_images/14s.jpg'), (128//3, 178//3))
hand_card_2 = pygame.transform.scale(pygame.image.load('deck_images/14h.jpg'), (128//3, 178//3))

while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()

    window.blit(player_1_surface, (win_width-(player_1_surface.get_width()+gap*3), win_height-(player_1_surface.get_height()+gap*3)))
    pygame.draw.rect(player_1_surface, (255, 255, 255), player_1_surface.get_rect(), 3)
    player_1_surface.blit(hand_card_1, (gap, gap))
    player_1_surface.blit(hand_card_2, (gap*2+128//3, gap))

    f1 = pygame.font.Font(None, 25)
    line_1 = f1.render("Player name", 0, (255, 255, 255))
    line_2 = f1.render("Chips amount: 1000", 0, (255, 255, 255))
    line_3 = f1.render("Bet 100 chips to continue!", 0, (255, 255, 255))

    player_1_surface.blit(line_1, (gap, gap*2 + 178 // 3))
    player_1_surface.blit(line_2, (gap, gap*4 + 178 // 3))
    player_1_surface.blit(line_3, (gap, gap*6 + 178 // 3))

    pygame.display.update()

    clock.tick(30)