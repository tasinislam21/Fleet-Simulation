import pygame
from pygame.math import Vector2
import networkx as nx
from drivable_road import DrivableRoad
import math

drivable_road = DrivableRoad()

def rotate_vector(vec, angle_degrees):
    angle = math.radians(angle_degrees)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return vec.__class__(
        vec.x * cos_a - vec.y * sin_a,
        vec.x * sin_a + vec.y * cos_a)

class BaseVehicle(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.current_sprite = 0
        self.sprites = sprites.copy()
        self.modified_sprites = [s.copy() for s in sprites]
        self.image = self.modified_sprites[self.current_sprite]
        self.image_pos = self.image.get_rect()
        self.start_node = drivable_road.get_random_node()
        self.end_node = drivable_road.get_random_node()
        self.get_safe_path()
        self.speed = 1.5
        self.image_pos.x = self.path[0][0] + 1
        self.image_pos.y = self.path[0][1] + 1
        self.pos = Vector2(self.path[0])
        self.target_radius = 50
        self.vel = Vector2(0, 0)
        self.current_path = 0
        self.angle = 0

    def flash_light(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.image_pos)

    def get_safe_path(self):
        number_of_tries = 0
        self.start_node = self.end_node
        while True:
            if number_of_tries >= 5:
                self.start_node = drivable_road.get_random_node()
            self.end_node = drivable_road.get_random_node()
            try:
                self.path, self.node_path = drivable_road.get_path(self.start_node, self.end_node)
                break
            except nx.NetworkXNoPath:
                number_of_tries += 1
                continue

    def get_new_dest(self):
        self.start_node = self.end_node
        self.get_safe_path()
        self.current_path = 0
        self.pos = pygame.Vector2(self.path[0])

    def can_it_move(self):
        if (self.current_path == len(self.path) - 1):
            return False
        target = pygame.Vector2(self.path[self.current_path+1])
        heading = target - self.pos
        distance = heading.length()

        if distance < 1:  # close enough → go to next waypoint
            self.current_path += 1
            return True

        heading.normalize_ip()
        self.speed = drivable_road.get_max_speed(self.node_path[self.current_path], self.node_path[self.current_path+1])
        step = min(self.speed, distance) - 0.1  # <-- prevents overshoot
        if distance <= self.target_radius and self.current_path == len(self.path) - 2:
            self.vel = heading * (
                        distance / self.target_radius * step)  # slow down when it reaches close to the destination
        else:
            self.vel = heading * step
        return True

    def rotate(self):
        if self.vel.length_squared() > 0:  # only rotate if moving
            target_angle = self.vel.angle_to(pygame.Vector2(0, -1))

            rotate_speed = 5
            diff = (target_angle - self.angle + 180) % 360 - 180  # shortest signed difference

            if abs(diff) > rotate_speed:
                self.angle += rotate_speed if diff > 0 else -rotate_speed
            else:
                self.angle = target_angle

            for i, image in enumerate(self.sprites):
                rotated = pygame.transform.rotate(image, self.angle)
                self.modified_sprites[i] = rotated
            self.image_pos = self.image.get_rect(center=self.pos)

    def front_clear(self, vehicles, safe_distance=40):
        for other in vehicles:
            if other is self:
                continue

            offset = other.pos - self.pos

            if offset.length_squared() == 0:  # Same position
                continue

            if self.vel.length_squared() > 0:
                forward = self.vel.normalize()
                if forward.dot(offset.normalize()) > 0.7:  # ~within 45° cone ahead
                    if offset.length() < safe_distance:
                        return False
        return True

    def avoid_blocker(self):
        # rotate velocity 20° left or right (could randomize to avoid all picking same side)
        self.vel = rotate_vector(self.vel, 20).normalize() * self.vel.length()
        self.pos += self.vel

    def update(self, vehicles):
        if self.can_it_move() and self.front_clear(vehicles) is True:
            self.pos += self.vel
        elif not self.can_it_move():
            self.get_new_dest()
        if self.front_clear(vehicles) is False:
            self.avoid_blocker()
        self.rotate()
        self.image_pos.center = self.pos
        if not self.isEmergency():
            self.image = self.modified_sprites[0]

    def isEmergency(self):
        return False

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos

class Police(BaseVehicle):
    def __init__(self, emergency):
        self.emergency = emergency
        if emergency:
            sprites = [
                pygame.image.load('images/response_police/police_red.png'),
                pygame.image.load('images/response_police/police_blue.png')
            ]
        else:
            sprites = [
                pygame.image.load('images/police.png')
            ]
        super().__init__(sprites)

    def isEmergency(self):
        return self.emergency

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.modified_sprites[int(self.current_sprite)]

class Car(BaseVehicle):
    def __init__(self):
        path = f"images/car.png"
        sprites = [pygame.image.load(path)]
        super().__init__(sprites)

class Bike(BaseVehicle):
    def __init__(self):
        path = f"images/bike.png"
        sprites = [pygame.image.load(path)]
        super().__init__(sprites)

class PoliceFactory:
    @staticmethod
    def create_vehicle(emergency):
        return Police(emergency)


class CarFactory:
    @staticmethod
    def create_vehicle():
        return Car()


class BikeFactory:
    @staticmethod
    def create_vehicle():
        return Bike()
