import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

going_up = False
going_left = False
going_right = False
going_down = False

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working With Rectangles")
default_car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.image.load("images/car.png").convert_alpha()

rect_1 = pygame.Rect(10, 10, 50, 320)
rect_2 = pygame.Rect(10, 300, 320, 50)
rect_3 = pygame.Rect(150, 180, 50, 120)
rect_4 = pygame.Rect(150, 180, 150, 50)
car_rect = car.get_rect()


def reset_direction():
    global going_up, going_left, going_right, going_down
    going_up = False
    going_left = False
    going_right = False
    going_down = False

def car_direction(current_position):
    global going_up, going_left, going_right, going_down
    global car
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] == True:
        car_rect.x -= 5
        if not going_left:
            car = pygame.transform.rotate(default_car, 90)
            reset_direction()
            going_left = True
    if key[pygame.K_RIGHT] == True:
        car_rect.x += 5
        if not going_right:
            car = pygame.transform.rotate(default_car, 270)
            reset_direction()
            going_right = True
    if key[pygame.K_UP] == True:
        car_rect.y -= 5
        if not going_up:
            car = default_car
            reset_direction()
            going_up = True
    if key[pygame.K_DOWN] == True:
        car_rect.y += 5
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
        #if event.type == pygame.MOUSEMOTION:
        #    print(f'Mouse position {event.pos}')

    pygame.draw.rect(screen, (255, 0, 255), rect_1)
    pygame.draw.rect(screen, (255, 0, 255), rect_2)
    pygame.draw.rect(screen, (255, 0, 255), rect_3)
    pygame.draw.rect(screen, (255, 0, 255), rect_4)
    car_direction(car_rect)
    screen.blit(car, car_rect)

    pygame.display.flip()
    screen.fill((0, 0, 0))

pygame.quit()