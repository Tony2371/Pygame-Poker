import pygame

pygame.init()


window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(15)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.aaline(window, (255,255,255) ,[100,100], [560, 700])


pygame.quit()