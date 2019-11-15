import pygame
from random import randint
pygame.init()

win_width = 400
window = pygame.display.set_mode((win_width,win_width))
clock = pygame.time.Clock()
running = True

class Snake():
	def __init__(self):
		self.surface = pygame.Surface((10,10))
		self.x_pos = 250
		self.y_pos = 250
		self.length = 1
		self.pos_list = []

	def draw(self):
		for i in self.pos_list:
			if i == self.pos_list[0]:
				window.blit(self.surface,i)
				pygame.draw.rect(self.surface,(50,150,255),self.surface.get_rect())

			else:
				window.blit(self.surface,i)
				pygame.draw.rect(self.surface,(255,255,255),self.surface.get_rect())
				pygame.draw.rect(self.surface,(0,0,0),self.surface.get_rect(),1)

class Food():
	def __init__(self):
		self.surface = pygame.Surface((10,10))
		self.x_pos = round(randint(0,win_width-2),-1)
		self.y_pos = round(randint(0,win_width-2),-1)
	def draw(self):
		window.blit(self.surface,(self.x_pos,self.y_pos))
		pygame.draw.rect(self.surface,(255,0,0),self.surface.get_rect())
	def change_position(self):
		self.x_pos = randint(0,win_width-1)//10*10
		self.y_pos = randint(0,win_width-1)//10*10

snake = Snake()
food = Food()
score = 0
direction = "RIGHT"
f1 = pygame.font.Font(None, 25)

while running:
	window.fill((45,0,45))

	speed = 10

	if direction == "RIGHT":
		snake.x_pos += speed
	if direction == "LEFT":
		snake.x_pos -= speed
	if direction == "UP":
		snake.y_pos -= speed
	if direction == "DOWN":
		snake.y_pos += speed


	snake.pos_list.insert(0,(snake.x_pos,snake.y_pos))
	
	print(snake.pos_list)

	if snake.x_pos == food.x_pos and snake.y_pos == food.y_pos:
		score += 1
		snake.length += 1
		food.change_position()
	
	if len(snake.pos_list) > snake.length:
		snake.pos_list.pop()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a and direction != "RIGHT":
				direction = "LEFT"
			if event.key == pygame.K_d and direction != "LEFT":
				direction = "RIGHT"
			if event.key == pygame.K_s and direction != "UP":
				direction = "DOWN"
			if event.key == pygame.K_w and direction != "DOWN":
				direction = "UP"

	#Loosing conditions
	if snake.pos_list.count((snake.x_pos,snake.y_pos)) == 2:
		running = False
	if snake.x_pos < 0 or snake.x_pos >= win_width or snake.y_pos < 0 or snake.y_pos >= win_width:
		running = False

	snake.draw()
	food.draw()
	text_1 = f1.render("Score: {0}".format(score), 0, (255, 255, 255))
	window.blit(text_1,(10,10))
	pygame.display.update()
	clock.tick(15)