import pygame
from map_generator import MapGenerator
from Vehicle import Vehicle
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Police vehicle simulator")
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))
map = MapGenerator("Random", SCREEN_WIDTH, SCREEN_HEIGHT)
minx, miny, maxx, maxy = map.get_map_bounds()
scale_x, scale_y = map.get_scale()

def normalize_coords(x, y):
    norm_x = int((x - minx) * scale_x)
    norm_y = int(SCREEN_HEIGHT - (y - miny) * scale_y)  # flip Y
    return (norm_x, norm_y)

def draw_map():
    buildings = map.get_buildings()
    for _, building in buildings.iterrows():
        xx, yy = building['geometry'].exterior.coords.xy
        building_coord = []
        for polygon_index in range(len(xx)):
            building_coord.append(normalize_coords(xx[polygon_index], yy[polygon_index]))
        pygame.draw.polygon(map_surface, (67, 255, 255), building_coord) # draws 1 building at a time

def draw_road():
    roads = map.get_road()
    for _, road in roads.iterrows():
        xx, yy = road['geometry'].coords.xy
        road_coord = []
        for polygon_index in range(len(xx)):
            road_coord.append(normalize_coords(xx[polygon_index], yy[polygon_index]))
        pygame.draw.lines(map_surface, (200, 5, 5), False, road_coord)

def get_road_coord():
    roads = map.get_road()
    full_road_coord = []
    for _, road in roads.iterrows():
        xx, yy = road['geometry'].coords.xy
        for polygon_index in range(len(xx)):
            full_road_coord.append(normalize_coords(xx[polygon_index], yy[polygon_index]))
    return full_road_coord

if __name__ == "__main__":
    full_road_coord = get_road_coord()
    draw_map()
    draw_road()
    vehicle = Vehicle(2, full_road_coord)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #if event.type == pygame.MOUSEMOTION:
            #    print(f'Mouse position {event.pos}')
        pygame.display.flip()
        screen.blit(map_surface, (0, 0))
        vehicle.render(screen)
        vehicle.update()
        if vehicle.isEmergency():
            vehicle.flash_light()
        clock.tick(60)

pygame.quit()