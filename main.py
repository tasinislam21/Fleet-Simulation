import pygame
from drivable_road import DrivableRoad
from map_generator import map_factory
from Vehicle import vehicle_factory
import argparse
import config as c
import random

parser = argparse.ArgumentParser()
parser.add_argument('--number_of_emergency_police', type=int, default=2)
parser.add_argument('--number_of_normal_police', type=int, default=10)
parser.add_argument('--number_civilian_car', type=int, default=6)
parser.add_argument('--number_civilian_bike', type=int, default=3)
args = parser.parse_args()

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

pygame.display.set_caption("Police vehicle simulator")
map_surface = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))
map = map_factory("Hackney")
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
    emergency_police_vehicles = []
    normal_police_vehicles = []

    for _ in range(args.number_of_emergency_police):
        temp = vehicle_factory('Police')
        temp.set_emergency(True)
        vehicles.add(temp)
        emergency_police_vehicles.append(temp)
    for _ in range(args.number_of_normal_police):
        temp = vehicle_factory('Police')
        vehicles.add(temp)
        normal_police_vehicles.append(temp)
    for _ in range(args.number_civilian_car):
        vehicles.add(vehicle_factory('Car'))
    for _ in range(args.number_civilian_bike):
        vehicles.add(vehicle_factory('Bike'))

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
            if vehicle.is_emergency():
                vehicle.flash_light()

        if len(normal_police_vehicles) > 0:
            normal_police_vehicle = normal_police_vehicles.pop(random.randrange(len(normal_police_vehicles)))
            if ((normal_police_vehicle.get_activity_time() > random.randrange(20, 40)) and
                    not normal_police_vehicle.is_emergency()):
                normal_police_vehicle.set_emergency(True)
                emergency_police_vehicles.append(normal_police_vehicle)
                normal_police_vehicle.render(screen)
                normal_police_vehicle.update(vehicles)
            else:
                normal_police_vehicles.append(normal_police_vehicle)

        if len(emergency_police_vehicles) > 0:
            emergency_police_vehicle = emergency_police_vehicles.pop(random.randrange(len(emergency_police_vehicles)))
            if ((emergency_police_vehicle.get_activity_time() > random.randrange(5, 15)) and
                    emergency_police_vehicle.is_emergency()):
                emergency_police_vehicle.set_emergency(False)
                normal_police_vehicles.append(emergency_police_vehicle)
                emergency_police_vehicle.render(screen)
                emergency_police_vehicle.update(vehicles)
            else:
                emergency_police_vehicles.append(emergency_police_vehicle)

        clock.tick(60)

pygame.quit()