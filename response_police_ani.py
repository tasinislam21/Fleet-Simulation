import pygame, sys

class ResponsePolice(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(pygame.image.load('images/response_police/police_red.png'))
		self.sprites.append(pygame.image.load('images/response_police/police_blue.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]
		self.rect = self.image.get_rect()

	def update(self,speed):
		self.current_sprite += speed
		if int(self.current_sprite) >= len(self.sprites):
			self.current_sprite = 0
		self.image = self.sprites[int(self.current_sprite)]

	def rotate(self, angle):
		self.image = pygame.transform.rotate(self.image, angle)




if __name__ == "__main__":
	pygame.init()
	clock = pygame.time.Clock()

	# Game Screen
	screen_width = 400
	screen_height = 400
	screen = pygame.display.set_mode((screen_width,screen_height))
	pygame.display.set_caption("Sprite Animation")

	# Creating the sprites and groups
	moving_sprites = pygame.sprite.Group()
	player = ResponsePolice()
	moving_sprites.add(player)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				player.attack()

		# Drawing
		screen.fill((0,0,0))
		moving_sprites.draw(screen)
		moving_sprites.update(0.15)
		pygame.display.flip()
		clock.tick(60)