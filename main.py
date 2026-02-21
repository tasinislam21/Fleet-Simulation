import pygame
from drivable_road import DrivableRoad
from map_generator import map_factory
from Vehicle import vehicle_factory
import argparse
import config as c
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument('--number_of_emergency_police', type=int, default=0)
parser.add_argument('--number_of_normal_police', type=int, default=5)
parser.add_argument('--number_civilian_car', type=int, default=10)
parser.add_argument('--number_civilian_bike', type=int, default=5)
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

def update_vehicles():
    for vehicle in vehicles:
        vehicle.render(screen)
        vehicle.update(vehicles)
        if vehicle.is_emergency():
            vehicle.flash_light()

def is_incident_due(incident_countdown):
    if (time.time() - incident_countdown > 2):
        return True
    else:
        return False

def create_incident():
    incident_list.append(time.time())

def assign_incident_to_vehicle():
    if len(incident_list) > 0 and len(normal_police_vehicles) > 0:
        normal_police_vehicle = normal_police_vehicles.pop(random.randrange(len(normal_police_vehicles)))
        incident = incident_list.pop(0)
        normal_police_vehicle.set_emergency(True, incident)
        emergency_police_vehicles.append(normal_police_vehicle)

def deallocation():
    emergency2normal = []
    for i, emergency_police_vehicle in enumerate(emergency_police_vehicles):  # check if reached destination
        if emergency_police_vehicle.reached_destination():
            emergency2normal.append(i)
    for i in emergency2normal:
        emergency_police_vehicle = emergency_police_vehicles.pop(i)
        response_times.append(emergency_police_vehicle.get_response_time())
        arrival_times.append(emergency_police_vehicle.get_arrival_time())
        del response_times[0]
        del arrival_times[0]
        emergency_police_vehicle.set_emergency(False)
        normal_police_vehicles.append(emergency_police_vehicle)

def show_avg_response_time():
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    avg_arrival_time = sum(arrival_times) / len(arrival_times) if arrival_times else 0
    incident_count = len(incident_list)

    output = (
        "Average response time: {:.2f} | "
        "Average arrival time: {:.2f} | "
        "Incident Queue: {}".format(avg_response_time, avg_arrival_time, incident_count)
    )

    print(output, end='\r', flush=True)

if __name__ == "__main__":
    draw_buildings()
    draw_road()
    drivable_road = DrivableRoad()
    drivable_road.set_graph(map.get_graph())
    drivable_road.set_node_positions(map.get_map_nodes())

    vehicles = pygame.sprite.Group()
    emergency_police_vehicles = []
    normal_police_vehicles = []
    incident_list = []
    incident_countdown = time.time()

    for _ in range(args.number_of_emergency_police):
        temp = vehicle_factory('Police')
        temp.set_emergency(True, time.time())
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
    response_times = [0 for i in range(10)]
    arrival_times = [0 for i in range(10)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        screen.blit(map_surface, (0, 0))
        update_vehicles()
        if is_incident_due(incident_countdown):
            create_incident()
            incident_countdown = time.time()
        assign_incident_to_vehicle()
        deallocation()
        show_avg_response_time()
        clock.tick(60)

pygame.quit()