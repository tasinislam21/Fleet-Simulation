import pygame
import config

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, car_image, speed, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.speed = speed
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        config.vehicles[direction][lane].append(self)
        self.index = len(config.vehicles[direction][lane]) - 1
        self.image = car_image
        if (direction == 'down'):
            self.image = pygame.transform.flip(self.image, False, True)
        elif (direction == 'left'):
            self.image = pygame.transform.rotate(self.image, 90)
        elif (direction == 'right'):
            self.image = pygame.transform.rotate(self.image, 270)

        if (len(config.vehicles[direction][lane]) > 1 and config.vehicles[direction][lane][
            self.index - 1].crossed == 0):  # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
            if (direction == 'right'):
                self.stop = config.vehicles[direction][lane][self.index - 1].stop - config.vehicles[direction][lane][
                    self.index - 1].image.get_rect().width - config.stoppingGap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            elif (direction == 'left'):
                self.stop = config.vehicles[direction][lane][self.index - 1].stop + config.vehicles[direction][lane][
                    self.index - 1].image.get_rect().width + config.stoppingGap
            elif (direction == 'down'):
                self.stop = config.vehicles[direction][lane][self.index - 1].stop - config.vehicles[direction][lane][
                    self.index - 1].image.get_rect().height - config.stoppingGap
            elif (direction == 'up'):
                self.stop = config.vehicles[direction][lane][self.index - 1].stop + config.vehicles[direction][lane][
                    self.index - 1].image.get_rect().height + config.stoppingGap
        else:
            self.stop = config.defaultStop[direction]

        # Set new starting and stopping coordinate
        if (direction == 'right'):
            temp = self.image.get_rect().width + config.stoppingGap
            config.x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image.get_rect().width + config.stoppingGap
            config.x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image.get_rect().height + config.stoppingGap
            config.y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image.get_rect().height + config.stoppingGap
            config.y[direction][lane] += temp
        config.simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.image.get_rect().width > config.stopLines[
                self.direction]):  # if the image has crossed stop line now
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and (
                    self.index == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane][self.index - 1].x - movingGap))):
                # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                self.x += self.speed  # move the vehicle
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]):
                self.crossed = 1
            if ((self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                    currentGreen == 1 and currentYellow == 0)) and (
                    self.index == 0 or self.y + self.image.get_rect().height < (
                    vehicles[self.direction][self.lane][self.index - 1].y - movingGap))):
                self.y += self.speed
        elif (self.direction == 'left'):
            if (self.crossed == 0 and self.x < stopLines[self.direction]):
                self.crossed = 1
            if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                    self.index == 0 or self.x > (
                    vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().width + movingGap))):
                self.x -= self.speed
        elif (self.direction == 'up'):
            if (self.crossed == 0 and self.y < stopLines[self.direction]):
                self.crossed = 1
            if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
                    self.index == 0 or self.y > (
                    vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().height + movingGap))):
                self.y -= self.speed
