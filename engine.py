import threading
import time
import pygame
import random

from map_generator import map_factory
from Vehicle import vehicle_factory
from drivable_road import DrivableRoad
from loading_screen import LoadingScreen

class Engine:
    def __init__(self, args, map_surface, screen):
        self.engine_ready = False
        self.args = args
        self.map_surface = map_surface
        self.screen = screen
        self.loading_screen = LoadingScreen()
        self.start_loading()

    def populate_times(self):
        self.incident_countdown = time.time()
        self.response_times = [0 for i in range(10)]
        self.arrival_times = [0 for i in range(10)]

    def populate_vehicles(self, args):
        self.vehicles = pygame.sprite.Group()
        self.emergency_police_vehicles = []
        self.normal_police_vehicles = []
        self.incident_list = []
        for _ in range(args.number_of_emergency_police):
            temp = vehicle_factory('Police')
            temp.set_emergency(True, time.time())
            self.vehicles.add(temp)
            self.emergency_police_vehicles.append(temp)
        for _ in range(args.number_of_normal_police):
            temp = vehicle_factory('Police')
            self.vehicles.add(temp)
            self.normal_police_vehicles.append(temp)
        for _ in range(args.number_civilian_car):
            self.vehicles.add(vehicle_factory('Car'))
        for _ in range(args.number_civilian_bike):
            self.vehicles.add(vehicle_factory('Bike'))

    def start_loading(self):
        thread = threading.Thread(target=self.load_assets)
        thread.start()

    def load_assets(self):
        # STEP 0
        self.loading_screen.set_progress(10, "Loading map...")
        self.load_map()

        # STEP 1
        self.loading_screen.set_progress(20, "Generating buildings...")
        self.draw_buildings()

        # STEP 2
        self.loading_screen.set_progress(35, "Generating road...")
        self.draw_road()

        # STEP 3
        self.loading_screen.set_progress(60, "Creating drivable road...")
        self.drivable_road = DrivableRoad()

        # STEP 4
        self.loading_screen.set_progress(80, "Setting graph...")
        self.drivable_road.set_graph(self.map.get_graph())

        # STEP 5
        self.loading_screen.set_progress(95, "Setting node positions...")
        self.drivable_road.set_node_positions(self.map.get_map_nodes())

        # DONE
        self.loading_screen.set_progress(100, "Done!")
        self.loading_screen.mark_done()

        self.populate_vehicles(self.args)
        self.populate_times()

        self.engine_ready = True

    def load_map(self):
        self.map = map_factory("Hackney")

    def draw_buildings(self):
        buildings = self.map.get_buildings_polygon()
        for building in buildings:
            pygame.draw.polygon(self.map_surface, (67, 255, 255), building)  # draws 1 building at a time

    def draw_road(self):
        roads = self.map.get_road_line()
        for road in roads:
            pygame.draw.lines(self.map_surface, (200, 5, 5), False, road, width=2)

    def update_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.render(self.screen)
            vehicle.update(self.vehicles)
            if vehicle.is_emergency():
                vehicle.flash_light()

    def is_incident_due(self, incident_countdown):
        if time.time() - incident_countdown > 4:
            return True
        else:
            return False

    def create_incident(self):
        self.incident_list.append(time.time())

    def assign_incident_to_vehicle(self):
        if len(self.incident_list) > 0 and len(self.normal_police_vehicles) > 0:
            normal_police_vehicle = self.normal_police_vehicles.pop(random.randrange(len(self.normal_police_vehicles)))
            incident = self.incident_list.pop(0)
            normal_police_vehicle.set_emergency(True, incident)
            self.emergency_police_vehicles.append(normal_police_vehicle)

    def deallocation(self):
        emergency2normal = []
        for i, emergency_police_vehicle in enumerate(self.emergency_police_vehicles):  # check if reached destination
            if emergency_police_vehicle.reached_destination():
                emergency2normal.append(i)
        for i in emergency2normal:
            emergency_police_vehicle = self.emergency_police_vehicles.pop(i)
            self.response_times.append(emergency_police_vehicle.get_response_time())
            self.arrival_times.append(emergency_police_vehicle.get_arrival_time())
            del self.response_times[0]
            del self.arrival_times[0]
            emergency_police_vehicle.set_emergency(False)
            self.normal_police_vehicles.append(emergency_police_vehicle)

    def show_avg_response_time(self):
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        avg_arrival_time = sum(self.arrival_times) / len(self.arrival_times) if self.arrival_times else 0
        incident_count = len(self.incident_list)

        output = (
            "Average response time: {:.2f} | "
            "Average arrival time: {:.2f} | "
            "Incident Queue: {}".format(avg_response_time, avg_arrival_time, incident_count)
        )

        print(output, end='\r', flush=True)


    def update(self):
        self.screen.blit(self.map_surface, (0, 0))
        self.update_vehicles()
        if self.is_incident_due(self.incident_countdown):
            self.create_incident()
            self.incident_countdown = time.time()
        self.assign_incident_to_vehicle()
        self.deallocation()
        self.show_avg_response_time()

    def get_engine_ready(self):
        return self.engine_ready

    def draw_loading_screen(self):
        self.loading_screen.draw(self.screen)
