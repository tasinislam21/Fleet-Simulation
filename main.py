import pygame

from drivable_road import DrivableRoad
from map_generator import MapGenerator
from Vehicle import PoliceFactory, CarFactory, BikeFactory
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Police vehicle simulator")
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))
map = MapGenerator("Random", SCREEN_WIDTH, SCREEN_HEIGHT)
minx, miny, maxx, maxy = map.get_map_bounds()
scale_x, scale_y = map.get_scale()

def draw_buildings():
    buildings = map.get_buildings_polygon()
    for building in buildings:
        pygame.draw.polygon(map_surface, (67, 255, 255), building) # draws 1 building at a time

def draw_road():
    roads = map.get_road_line()
    for road in roads:
        pygame.draw.lines(map_surface, (200, 5, 5), False, road, width= 5)

if __name__ == "__main__":
    draw_buildings()
    draw_road()
    drivable_road = DrivableRoad()
    drivable_road.set_drivable_road(map.get_road_coord())
    vehicles = []
    police_factory = PoliceFactory()
    car_factory = CarFactory()
    bike_factory = BikeFactory()

    vehicles.append(police_factory.create_vehicle(True))
    vehicles.append(police_factory.create_vehicle(False))
    vehicles.append(car_factory.create_vehicle())
    vehicles.append(bike_factory.create_vehicle())
    vehicles.append(bike_factory.create_vehicle())
    vehicles.append(bike_factory.create_vehicle())
    vehicles.append(bike_factory.create_vehicle())
    while True:
        pygame.display.flip()
        screen.blit(map_surface, (0, 0))
        for vehicle in vehicles:
            vehicle.render(screen)
            vehicle.update()
            if vehicle.isEmergency():
                vehicle.flash_light()
        clock.tick(60)

pygame.quit()