import pygame
import config as c

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicle_id, direction_number):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.speed = c.speeds[c.vehicleTypes[vehicle_id]]
        self.direction = c.directionNumbers[direction_number]
        self.emergency = True if vehicle_id == 2 else False
        self.x = c.x[self.direction][lane]
        self.y = c.y[self.direction][lane]
        self.crossed = 0
        c.vehicles[self.direction][lane].append(self)
        self.index = len(c.vehicles[self.direction][lane]) - 1
        self.sprites = []
        if (vehicle_id == 2):
            self.sprites.append(pygame.image.load('images/response_police/police_red.png'))
            self.sprites.append(pygame.image.load('images/response_police/police_blue.png'))
        else:
            path = "images/" + c.vehicleTypes[vehicle_id] + ".png"
            self.sprites.append(pygame.image.load(path))

        for car_index in range(len(self.sprites)):
            if (self.direction == 'down'):
                self.sprites[car_index] = pygame.transform.flip(self.sprites[car_index], False, True)
            elif (self.direction == 'left'):
                self.sprites[car_index] = pygame.transform.rotate(self.sprites[car_index], 90)
            elif (self.direction == 'right'):
                self.sprites[car_index] = pygame.transform.rotate(self.sprites[car_index], 270)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        if (len(c.vehicles[self.direction][lane]) > 1 and c.vehicles[self.direction][lane][
            self.index - 1].crossed == 0):  # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
            if (self.direction == 'right'):
                self.stop = c.vehicles[self.direction][lane][self.index - 1].stop - c.vehicles[self.direction][lane][
                    self.index - 1].image.get_rect().width - c.stoppingGap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            elif (self.direction == 'left'):
                self.stop = c.vehicles[self.direction][lane][self.index - 1].stop + c.vehicles[self.direction][lane][
                    self.index - 1].image.get_rect().width + c.stoppingGap
            elif (self.direction == 'down'):
                self.stop = c.vehicles[self.direction][lane][self.index - 1].stop - c.vehicles[self.direction][lane][
                    self.index - 1].image.get_rect().height - c.stoppingGap
            elif (self.direction == 'up'):
                self.stop = c.vehicles[self.direction][lane][self.index - 1].stop + c.vehicles[self.direction][lane][
                    self.index - 1].image.get_rect().height + c.stoppingGap
        else:
            self.stop = c.defaultStop[self.direction]

        # Set new starting and stopping coordinate
        if (self.direction == 'right'):
            temp = self.image.get_rect().width + c.stoppingGap
            c.x[self.direction][lane] -= temp
        elif (self.direction == 'left'):
            temp = self.image.get_rect().width + c.stoppingGap
            c.x[self.direction][lane] += temp
        elif (self.direction == 'down'):
            temp = self.image.get_rect().height + c.stoppingGap
            c.y[self.direction][lane] -= temp
        elif (self.direction == 'up'):
            temp = self.image.get_rect().height + c.stoppingGap
            c.y[self.direction][lane] += temp

    def update(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, currentGreen, currentYellow):
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.image.get_rect().width > c.stopLines[
                self.direction]):  # if the image has crossed stop line now
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and (
                    self.index == 0 or self.x + self.image.get_rect().width < (
                    c.vehicles[self.direction][self.lane][self.index - 1].x - c.movingGap))):
                # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                self.x += self.speed  # move the vehicle
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.image.get_rect().height > c.stopLines[self.direction]):
                self.crossed = 1
            if ((self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                    currentGreen == 1 and currentYellow == 0)) and (
                    self.index == 0 or self.y + self.image.get_rect().height < (
                    c.vehicles[self.direction][self.lane][self.index - 1].y - c.movingGap))):
                self.y += self.speed
        elif (self.direction == 'left'):
            if (self.crossed == 0 and self.x < c.stopLines[self.direction]):
                self.crossed = 1
            if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                    self.index == 0 or self.x > (
                    c.vehicles[self.direction][self.lane][self.index - 1].x + c.vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().width + c.movingGap))):
                self.x -= self.speed
        elif (self.direction == 'up'):
            if (self.crossed == 0 and self.y < c.stopLines[self.direction]):
                self.crossed = 1
            if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
                    self.index == 0 or self.y > (
                    c.vehicles[self.direction][self.lane][self.index - 1].y + c.vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().height + c.movingGap))):
                self.y -= self.speed
    def isEmergency(self):
        return self.emergency

    def get_object(self):
        return self