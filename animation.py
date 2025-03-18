import pygame
import os

def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images

class AnimatedResponsePolice(pygame.sprite.Sprite):
    def __init__(self, position):
        super(AnimatedResponsePolice, self).__init__()
        size = (54, 22)  # This should match the size of the images.
        self.rect = pygame.Rect(position, size)
        images = load_images('images/response_police')
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.
        self.animation_time = 0.1
        self.current_time = 0
        self.animation_frames = 6
        self.current_frame = 0

    def update_frame_dependent(self):
        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self, dt):
        self.update_time_dependent(dt)
