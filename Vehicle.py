import pygame
import config as c

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vehicle_id):
        pygame.sprite.Sprite.__init__(self)
        self.emergency = True if vehicle_id == 2 else False
        self.sprites = []
        if (vehicle_id == 2):
            self.sprites.append(pygame.image.load('images/response_police/police_red.png'))
            self.sprites.append(pygame.image.load('images/response_police/police_blue.png'))
        else:
            path = "images/" + c.vehicleTypes[vehicle_id] + ".png"
            self.sprites.append(pygame.image.load(path))

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.ori_image = self.sprites[self.current_sprite]

        self.image_pos = self.image.get_rect()
        self.image_pos.center = (454, 203)

        self.going_up = False
        self.going_left = False
        self.going_right = False
        self.going_down = False

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

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
                self.image = pygame.transform.rotate(self.ori_image, 90)
                self.reset_direction()
                self.going_left = True
        if key[pygame.K_RIGHT] == True:
            self.image_pos.x += 5
            if not self.going_right:
                self.image = pygame.transform.rotate(self.ori_image, 270)
                self.reset_direction()
                self.going_right = True
        if key[pygame.K_UP] == True:
            self.image_pos.y -= 5
            if not self.going_up:
                self.image = self.ori_image
                self.reset_direction()
                self.going_up = True
        if key[pygame.K_DOWN] == True:
            self.image_pos.y += 5
            if not self.going_down:
                self.image = pygame.transform.rotate(self.ori_image, 180)
                self.reset_direction()
                self.going_down = True

    def isEmergency(self):
        return self.emergency

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos