import pygame
from pygame.math import Vector2
import networkx as nx
from pygments.lexers import q

from drivable_road import DrivableRoad
import math
import time

drivable_road = DrivableRoad()

###### Load sprites into memory once#########
car_sprites = [pygame.image.load("images/car.png")]
bike_sprites = [pygame.image.load("images/bike.png")]
police_normal_sprites = [pygame.image.load("images/police.png")]
police_emergency_sprites = [
                pygame.image.load('images/response_police/police_red.png'),
                pygame.image.load('images/response_police/police_blue.png')
            ]

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
        self.current_position = Vector2(self.path[0])
        self.target_radius = 50
        self.vel = Vector2(0, 0)
        self.distance2target = Vector2()
        self.current_path = 0
        self.angle = 0

    def flash_light(self):
        pass

    def set_emergency(self, state: bool):
        pass

    def reload_sprites(self):
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

    def update_new_dest(self):
        self.start_node = self.end_node
        self.get_safe_path()
        self.current_path = 0
        self.current_position = pygame.Vector2(self.path[0])

    def update_distance_to_target(self):
        target_position = pygame.Vector2(self.path[self.current_path + 1])
        self.distance2target = target_position - self.current_position

    def update_velocity(self):
        distance = self.distance2target.length()
        self.distance2target.normalize_ip()
        self.speed = drivable_road.get_max_speed(self.node_path[self.current_path -1],
                                                 self.node_path[self.current_path])
        step = min(self.speed, distance) - 0.1  # <-- prevents overshoot
        if distance <= self.target_radius and self.current_path == len(self.path) - 2:
            self.vel = self.distance2target * (
                    distance / self.target_radius * step)  # slow down when it reaches close to the destination
        else:
            self.vel = self.distance2target * step

    def update_edge(self):
        self.update_distance_to_target()
        distance = self.distance2target.length()
        if distance < 1:  # close enough → go to next waypoint
            self.current_path += 1

    def reached_destination(self):
        if (self.current_path == len(self.path) - 1):
            return True
        else:
            return False

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
            self.image_pos = self.image.get_rect(center=self.current_position)

    def front_clear(self, vehicles, safe_distance=40, min_ignore_distance=5):
        for other in vehicles:
            if other is self:
                continue

            offset = other.current_position - self.current_position
            offset_length = offset.length()

            if offset_length < min_ignore_distance:
                return True  # Too close — consider overlapping

            if self.vel.length_squared() > 0:
                forward = self.vel.normalize()
                if forward.dot(offset.normalize()) > 0.7:  # Within ~45° cone in front
                    if offset_length < safe_distance:
                        return False

        return True

    def slow_down(self):
        self.current_position += self.vel * 0.4

    def update(self, vehicles):
        if not self.reached_destination():
            self.update_edge()
            self.update_velocity()
            if self.front_clear(vehicles):
                self.current_position += self.vel
            else:
                self.slow_down()
        elif self.reached_destination():
            self.update_new_dest()
        self.rotate()
        self.image_pos.center = self.current_position
        if not self.is_emergency():
            self.image = self.modified_sprites[0]

    def is_emergency(self):
        return False

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos

    def get_response_time(self):
        return 0

class Police(BaseVehicle):
    def __init__(self):
        self.emergency = False
        self.activity_time = 0
        super().__init__(police_normal_sprites)

    def is_emergency(self):
        return self.emergency

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.modified_sprites[int(self.current_sprite)]

    def set_emergency(self, state: bool):
        self.emergency = state
        self.activity_time = time.time()
        self.reload_sprites()

    def reload_sprites(self):
        if self.emergency:
            sprites = police_emergency_sprites
        else:
            sprites = police_normal_sprites
        self.current_sprite = 0
        self.sprites = sprites.copy()
        self.modified_sprites = [s.copy() for s in sprites]
        self.image = self.modified_sprites[self.current_sprite]
        self.image_pos = self.image.get_rect()

    def get_response_time(self):
        return time.time() - self.activity_time

    def slow_down(self):
        if self.emergency:
            self.current_position += self.vel * 0.8
        else:
            self.current_position += self.vel * 0.4

class Car(BaseVehicle):
    def __init__(self):
        super().__init__(car_sprites)

class Bike(BaseVehicle):
    def __init__(self):
        super().__init__(bike_sprites)

def vehicle_factory(type ="Car"):
    localizers = {
        "Car": Car,
        "Bike": Bike,
        "Police": Police,
    }
    return localizers[type]()