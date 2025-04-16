import pygame
import config as c

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vehicle_id):
        pygame.sprite.Sprite.__init__(self)
        self.emergency = True if vehicle_id == 2 else False
        sprites = []
        if (vehicle_id == 2):
            sprites.append(pygame.image.load('images/response_police/police_red.png'))
            sprites.append(pygame.image.load('images/response_police/police_blue.png'))
        else:
            path = "images/" + c.vehicleTypes[vehicle_id] + ".png"
            sprites.append(pygame.image.load(path))

        self.current_sprite = 0

        self.ori_image = sprites.copy()
        self.direction_image = sprites.copy()
        self.image = self.direction_image[self.current_sprite]

        self.image_pos = self.image.get_rect()
        self.image_pos.center = (454, 203)

        self.going_up = False
        self.going_left = False
        self.going_right = False
        self.going_down = False

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.direction_image):
            self.current_sprite = 0
        self.image = self.direction_image[int(self.current_sprite)]

    def render(self, screen):
        screen.blit(self.image, self.image_pos)

    def reset_direction(self):
        self.going_up = False
        self.going_left = False
        self.going_right = False
        self.going_down = False

    def move(self, key):
        if key[pygame.K_LEFT] == True:
            self.image_pos.x -= 5
            if not self.going_left:
                for i, image in enumerate(self.ori_image):
                    self.direction_image[i] = pygame.transform.rotate(image, 90)
                self.image = self.direction_image[0]
                self.reset_direction()
                self.going_left = True
        if key[pygame.K_RIGHT] == True:
            self.image_pos.x += 5
            if not self.going_right:
                for i, image in enumerate(self.ori_image):
                    self.direction_image[i] = pygame.transform.rotate(image, 270)
                self.image = self.direction_image[0]
                self.reset_direction()
                self.going_right = True
        if key[pygame.K_UP] == True:
            self.image_pos.y -= 5
            if not self.going_up:
                for i, image in enumerate(self.ori_image):
                    self.direction_image[i] = image
                self.image = self.direction_image[0]
                self.reset_direction()
                self.going_up = True
        if key[pygame.K_DOWN] == True:
            self.image_pos.y += 5
            if not self.going_down:
                for i, image in enumerate(self.ori_image):
                    self.direction_image[i] = pygame.transform.rotate(image, 180)
                self.image = self.direction_image[0]
                self.reset_direction()
                self.going_down = True

    def isEmergency(self):
        return self.emergency

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos