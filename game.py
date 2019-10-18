import pygame

pygame.init()

window = pygame.display.set_mode((640,480))

pygame.display.set_caption("Game")
clock = pygame.time.Clock()

def draw_text(text, position):
    f1 = pygame.font.Font(None,32)
    text1 = f1.render(text,1,(100,100,250))
    window.blit(text1,position)

x = 4
y = 10

running = True
cards_generated = 0

while running:
    clock.tick(15)    
    draw_text("My name is INNOVATION",(150,300))
    
    while cards_generated < 53:	    
	    for l in range(4):
	    	cards_generated += 1
	    	y += 45
	    	x = 4
	    	for m in range(13):
	    		cards_generated += 1
		    	x += 40
		    	x_size = 63.5
		    	y_size = 89
		    	pygame.draw.rect(window,(0,255,180),(x,y,x_size*0.4,y_size*0.4))



	

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()

pygame.quit()