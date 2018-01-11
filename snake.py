import pygame
import sys
import random
import time
import enum
import math

from enum import Enum

VERTICAL_BOUNDARIES = [0, 490]
HORIZONTAL_BOUNDARIES = [0, 490]
SIZE = 10

class Direction(Enum):
	UP = 0
	DOWN = 1
	RIGHT = 2
	LEFT = 3

class Snake():
	def __init__(self):
		self.position = [100, 50]
		self.body = [[100, 50], [90, 50], [80, 50]]
		self.direction = Direction.RIGHT
		self.changeDirectionTo = self.direction

	def changeDirTo(self, dir):
		if dir == Direction.RIGHT and self.direction != Direction.LEFT:
			self.direction = Direction.RIGHT
		elif dir == Direction.LEFT and self.direction != Direction.RIGHT:
			self.direction = Direction.LEFT
		elif dir == Direction.UP and self.direction != Direction.DOWN:
			self.direction = Direction.UP
		elif self.direction != Direction.UP:
			self.direction = Direction.DOWN

	def move(self, foodPosition):
		if self.direction == Direction.RIGHT:
			self.position[0] += SIZE
		elif self.direction == Direction.LEFT:
			self.position[0] -= SIZE
		elif self.direction == Direction.UP:
			self.position[1] -= SIZE
		elif self.direction == Direction.DOWN:
			self.position[1] += SIZE
		self.body.insert(0, list(self.position))	
		if self.position == foodPosition:
			return True
		else:
			self.body.pop()
			return False

	def isCollision(self):
		if self.position[0] < VERTICAL_BOUNDARIES[0] or self.position[0] > VERTICAL_BOUNDARIES[1]:
			return True
		elif self.position[1] < HORIZONTAL_BOUNDARIES[0] or self.position[1] > VERTICAL_BOUNDARIES[1]:
			return True
		for part in self.body[1:]:
			if self.position == part:
				return True
		else:
			return False

	def getHeadPos(self):
		return self.position

	def getBody(self):
		return self.body

class Food():

	def roundup(x):
		return int(math.ceil(x/10.0)) * 10

	def __init__(self):
		self.position = [random.randint(VERTICAL_BOUNDARIES[0],VERTICAL_BOUNDARIES[1]/10) * 10, random.randint(HORIZONTAL_BOUNDARIES[0], HORIZONTAL_BOUNDARIES[1] / 10) * 10]
		self.isFoodSpawned = True

	def spawnFood(self):
		if self.isFoodSpawned == False:
			self.position = [random.randint(VERTICAL_BOUNDARIES[0],VERTICAL_BOUNDARIES[1]/10) * 10, random.randint(HORIZONTAL_BOUNDARIES[0], HORIZONTAL_BOUNDARIES[1] / 10) * 10]
			self.isFoodSpawned = True
		return self.position

	def setFoodSpawnedStatus(self, status):
		self.isFoodSpawned = status


window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake PPP")
fps = pygame.time.Clock()

score = 0

snake = Snake()
food = Food()

def gameOver():
	pygame.init()
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("Some text!", 1, (255,255,0))
	screen.blit(label, (100, 100))
	pygame.quit()
	sys.exit()
	

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				snake.changeDirTo(Direction.RIGHT)
			elif event.key == pygame.K_LEFT:
				snake.changeDirTo(Direction.LEFT)
			elif event.key == pygame.K_DOWN:
				snake.changeDirTo(Direction.DOWN)
			elif event.key == pygame.K_UP:
				snake.changeDirTo(Direction.UP)

	foodPosition = food.spawnFood()
	if snake.move(foodPosition):
		food.setFoodSpawnedStatus(False)
	window.fill(pygame.Color(0, 0, 0))
	for pos in snake.getBody():
		pygame.draw.rect(window, pygame.Color(0, 225, 0), pygame.Rect(pos[0], pos[1], 10, 10))
	pygame.draw.rect(window, pygame.Color(225, 0, 0), pygame.Rect(foodPosition[0], foodPosition[1], 10, 10))
	if(snake.isCollision()):
		gameOver()

	pygame.display.flip()
	fps.tick(12)
