import pygame
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

going_up = False
going_left = False
going_right = False
going_down = False

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))
pygame.display.set_caption("Buildings")
default_car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.image.load("images/car.png").convert_alpha()

buildings = [
    #           x  y   w    h
    pygame.Rect(0, 0, 300, 200),
    pygame.Rect(360, 0, 200, 150),
    pygame.Rect(620, 0, 880, 200),
    pygame.Rect(0, 260, 420, 100),
    pygame.Rect(490, 285, 300, 150),
    pygame.Rect(850, 260, 300, 150),
    pygame.Rect(0, 450, 300, 150),
]
for wall in buildings:
    pygame.draw.rect(map_surface, (255, 255, 255), wall)

car_rect = car.get_rect()
car_rect.center = (454, 203)

def reset_direction():
    global going_up, going_left, going_right, going_down
    going_up = False
    going_left = False
    going_right = False
    going_down = False

def move_car():
    global going_up, going_left, going_right, going_down
    global car

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] == True:
        car_rect.x -= 5
        if car_rect.collidelist(buildings) >= 0:
            car_rect.x += 5
        if not going_left:
            car = pygame.transform.rotate(default_car, 90)
            reset_direction()
            going_left = True
    if key[pygame.K_RIGHT] == True:
        car_rect.x += 5
        if car_rect.collidelist(buildings) >= 0:
            car_rect.x -= 5
        if not going_right:
            car = pygame.transform.rotate(default_car, 270)
            reset_direction()
            going_right = True
    if key[pygame.K_UP] == True:
        car_rect.y -= 5
        if car_rect.collidelist(buildings) >= 0:
            car_rect.y += 5
        if not going_up:
            car = default_car
            reset_direction()
            going_up = True
    if key[pygame.K_DOWN] == True:
        car_rect.y += 5
        if car_rect.collidelist(buildings) >= 0:
            car_rect.y -= 5
        if not going_down:
            car = pygame.transform.rotate(default_car, 180)
            reset_direction()
            going_down = True



run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            print(f'Mouse position {event.pos}')


    move_car()
    if car_rect.collidelist(buildings) >= 0:
        print("car hit")
    screen.blit(map_surface, (0, 0))
    screen.blit(car, car_rect)
    pygame.display.flip()

pygame.quit()