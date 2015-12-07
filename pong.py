#!/usr/bin/env python2.7-32
# Make sure what envirement is using

#PiPong - A remake of the classic Pong game using PyGame

import pygame # Provides what we need to make a game
import sys # Gives us the sys.exit function to close our program
import random # Can generate random positions for the pong ball


from pygame.locals import *

# our main game class
class PiPong:

	def __init__(self):

		# make the display size a memeber of the class
		self.displaySize =  (640, 480)

		pygame.init()

		self.Clock = pygame.time.Clock()

		pygame.display.set_caption("Pi Pong")

		self.display = pygame.display.set_mode(self.displaySize)

		Ball(self.displaySize)

	def handleEvents(self):

		# handle events, starting with the quit event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				# Find what key is pressed and start moving
				if event.key == K_s:
					# Start moving bat
					self.player1Bat.startMove("down")
				elif event.key == K_w:
					# Start moving bat
					self.player1Bat.startMove("up")

				if event.key == K_DOWN:
					# Start moving bat
					self.player2Bat.startMove("down")
				elif event.key == K_UP:
					# Start moving bat
					self.player2Bat.startMove("up")

				if event.key == K_s or event.key == K_w:
					self.player1Bat.stopMove()
				elif event.key == K_DOWN or event.key == K_UP:
					self.player2Bat.stopMove()

	def run(self):
		while True:
			# Handle Events
			self.handleEvents()

			# Draw the background
			background.draw(self.displaySize)

			self.ball.batCollisionTest(self.player1Bat)
			self.ball.batCollisionTest(self.player2Bat)

			# Update and draw the sprites
			self.sprites.update()
			self.sprites.draw(self.display)

class Ball(pygame.sprite.Sprite):

	def __init__(self, displaySize):

		# Initialize the sprite base class
		super(Ball, self).__init__()

		# Get the display size for working out collisions later
		self.display = displaySize

		# Get a width and height values proportionate to the display size
		width = displaySize[0] / 30
		height = displaySize[1] / 30

		# Create an image for the sprite
		self.image = Surface((width, height))

		# Fill the image blue
		self.image.fill((27, 244, 198))

		# Create the sprites rectangle from the image
		self.rect = self.image.get_rect()

		# Work out a speed
		self.speed = displaySize[0] / 110

		# Reset the ball
		self.reset()

	def batCollisionTest(self, bat):

		# Check if the ball has had a collision with the bat
		if Rect.colliderect(bat.rect, self.rect):

			# Work out the difference between the start and end points
			deltaX = self.rect.centerx - bat.rect.centerx
			deltaY = self.rect.centery - bat.rect.centery

			# Make the values smaller so it's not too fast
			deltaX = deltaX / 12
			deltaY = deltaY / 12

			# Set the balls new direction
			self.vector = (deltaX, deltaY)

	def reset(self):

		# Start the ball directly in the center of the screen
		self.rect.centerx = self.displaySize[0] / 2
		self.rect.centery = self.displaySize[1] / 2

		# Start the ball moving to the left or right (pick randomly)
		# vector x,y
		if random.randrange(1, 3) == 1:
			# Move to left
			self.vector = (-1, 0)
		else:
			# Move to right
			self.vector = (1, 0)

	def update(self):

		# Check if the ball has hit the wall
		if self.rect.midtop[1] <= 0:
			# Hit top side
			self.reflectVector()

		elif self.rect.midleft[0] <= 0:
			# Hit left side
			self.reset()
		elif self.rect.midright[0] >= self.displaySize[0]:
			self.reset()
		elif self.rect.midbottom[1] >= self.displaySize[1]:
			self.reflectVector()

		# Move in the direction of the vector
		self.rect.centerx += (self.vector[0] * self.speed)
		self.rect.centery += (self.vector[1] * self.speed)


class Bat(pygame.sprite.Sprite):

	def __init__(self, displaySize, player):

		# Initialize the sprite base class
		super(Bat, self).__init__()
		# Make player a member variable
		self.player = player

		# Get a width and height values proportionate to the display size
		width = displaySize[0] / 80
		height = displaySize[1] / 6

		# Create an image for the sprite using the width and height we just worked out
		self.image = Surface((width, height))

		# Fill the image white
		self.image.fill((255, 255, 255))

		# Create the sprites rectangle from the image
		self.rect = self.image.get_rect()

		# Set the rectangle's location depending on the player
		if player == "player1":
			# Left side
			self.rect.centerx = displaySize[0] / 20
		elif player == "player2":
			# Right side
			self.rect.centerx = displaySize[0] - displaySize[0] / 20

		# Center the rectangle vertically
		self.rect.centerx = displaySize[1] / 2
		# Set a bunch of direction and moving variables
		self.moving = false
		self.direction = "none"
		self.speed = 13

	def startMove(self, direction):

		# Set the moving flag to true
		self.direction = direction
		self.moving = true

	def update(self):
		
		if self.moving:
			# Move the bat up or down if moving
			if self.direction == 'up':
				self.rect.centery -= self.speed
			elif self.direction == 'down':
				self.rect.centery += self.speed

	def stopMove(self):
		self.moving = false

class background:

	def __init__(self, displaySize):

		# set our image to a new surface, the size of the screen recatangle
		self.image = Surface(displaySize)

		# fill the image with a green color (specified as r,g,b)
		self.image.fill((27, 210, 57))

		# Get width proportionate to display size
		lineWidth = displaySize[0] / 80

		# Create a rectangle to make the white line
		lineRect = rect(0, 0, lineWidth, displaySize[1])
		lineRect.centerx = displaySize[0] / 2
		draw.rect(self.image, (255, 255, 255), lineRect)

		self.background = background(self.displaySize)

	def draw(self, display):

		# Draw the background to the display that has been passed in
		display.blit(self.image, (0,0))

		# Create two bats and add them to a sprite group
		self.player1Bat = Bat(self.displaySize, "player1")
		self.player2Bat = Bat(self.displaySize, "player2")
		self.sprites = sprite.Group(self.player1Bat, self.player2Bat)

if __name__ == '__main__':
	game = PiPong()
	game.run()


