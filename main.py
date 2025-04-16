import pygame
from map_generator import MapGenerator
from Vehicle import Vehicle

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

going_up = False
going_left = False
going_right = False
going_down = False

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Police vehicle simulator")
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))
map = MapGenerator("Random", SCREEN_WIDTH, SCREEN_HEIGHT)
minx, miny, maxx, maxy = map.get_map_bounds()
scale = map.get_scale()

vehicle = Vehicle(2)

def normalize_coords(x, y):
    norm_x = int((x - minx) * scale)
    norm_y = int(SCREEN_HEIGHT - (y - miny) * scale)  # flip Y
    return (norm_x, norm_y)

def draw_map():
    buildings = map.get_buildings()
    for _, building in buildings.iterrows():
        xx, yy = building['geometry'].exterior.coords.xy
        building_coord = []
        for polygon_index in range(len(xx)):
            building_coord.append(normalize_coords(xx[polygon_index], yy[polygon_index]))
        pygame.draw.polygon(map_surface, (67, 255, 255), building_coord) # draws 1 building at a time

def direction_key_handling():
    key = pygame.key.get_pressed()
    vehicle.move(key)

run = True
draw_map()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #if event.type == pygame.MOUSEMOTION:
        #    print(f'Mouse position {event.pos}')
    pygame.display.flip()
    screen.blit(map_surface, (0, 0))
    vehicle.render(screen)
    direction_key_handling()
    if vehicle.isEmergency():
        vehicle.flash_light()
    clock.tick(60)

pygame.quit()