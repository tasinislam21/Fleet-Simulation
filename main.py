import pygame
import geopandas
import osmnx as ox
from shapely.geometry import box

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

going_up = False
going_left = False
going_right = False
going_down = False

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working With Rectangles")
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))

place_name = "Hackney, UK"
hackney = ox.geocode_to_gdf(place_name)
polygon = box(-0.1, 51.57, -0.08, 51.56)
poly_gdf = geopandas.GeoDataFrame([1], geometry=[polygon])
hackney_clipped = hackney.clip(polygon)
building_tags = {"building": True}
buildings = ox.features_from_polygon(hackney_clipped['geometry'].iloc[0], building_tags)
minx, miny, maxx, maxy = buildings.total_bounds

default_car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.image.load("images/car.png").convert_alpha()
car_rect = car.get_rect()
car_rect.center = (454, 203)

scale_x = SCREEN_WIDTH / (maxx - minx)
scale_y = SCREEN_HEIGHT / (maxy - miny)
scale = min(scale_x, scale_y)

def normalize_coords(x, y):
    """Convert from geo coords to screen coords"""
    norm_x = int((x - minx) * scale)
    norm_y = int(SCREEN_HEIGHT - (y - miny) * scale)  # flip Y
    return (norm_x, norm_y)

# Draw map
for _, building in buildings.iterrows():
    xx, yy = building['geometry'].exterior.coords.xy
    building_coord = []
    for polygon_index in range(len(xx)):
        building_coord.append(normalize_coords(xx[polygon_index], yy[polygon_index]))
    pygame.draw.polygon(map_surface, (67, 255, 255), building_coord)



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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #if event.type == pygame.MOUSEMOTION:
        #    print(f'Mouse position {event.pos}')
    move_car()
    pygame.display.flip()
    screen.blit(map_surface, (0, 0))
    screen.blit(car, car_rect)

    clock.tick(60)

pygame.quit()