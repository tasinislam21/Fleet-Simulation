import pygame
from drivable_road import DrivableRoad
from map_generator import MapGenerator
from Vehicle import PoliceFactory, CarFactory, BikeFactory
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--number_of_emergency_police', type=int, default=3)
parser.add_argument('--number_of_normal_police', type=int, default=7)
parser.add_argument('--number_civilian_car', type=int, default=15)
parser.add_argument('--number_civilian_bike', type=int, default=7)
args = parser.parse_args()

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
    drivable_road.set_graph(map.get_graph())
    drivable_road.set_node_positions(map.get_map_nodes())

    vehicles = pygame.sprite.Group()
    police_factory = PoliceFactory()
    car_factory = CarFactory()
    bike_factory = BikeFactory()
    for _ in range(args.number_of_emergency_police):
        vehicles.add(police_factory.create_vehicle(True))
    for _ in range(args.number_of_normal_police):
        vehicles.add(police_factory.create_vehicle(False))
    for _ in range(args.number_civilian_car):
        vehicles.add(car_factory.create_vehicle())
    for _ in range(args.number_civilian_bike):
        vehicles.add(bike_factory.create_vehicle())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        screen.blit(map_surface, (0, 0))
        for vehicle in vehicles:
            vehicle.render(screen)
            vehicle.update(vehicles)
            if vehicle.isEmergency():
                vehicle.flash_light()
        clock.tick(60)

pygame.quit()