import pygame

pygame.init()

window = pygame.display.set_mode((800,600))

pygame.display.set_caption("Game")
clock = pygame.time.Clock()

running = True
y = 100
x = 100

while running:
    clock.tick(15)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(window, (0,255,55),(400,200,63.5,88.8))

    pygame.display.update()


pygame.quit()