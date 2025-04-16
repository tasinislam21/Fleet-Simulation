import osmnx as ox
from shapely.geometry import box

class MapGenerator:
    def __init__(self, place_name, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.place_name = place_name
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        place_name = "Hackney, UK" # temp
        area = ox.geocode_to_gdf(place_name)
        polygon = box(-0.1, 51.57, -0.08, 51.56) # temp
        self.area = area.clip(polygon) # temp
        self.calculate_scale()

    def calculate_scale(self):
        self.minx, self.miny, self.maxx, self.maxy = self.area.total_bounds
        GEO_WIDTH = self.maxx - self.minx
        GEO_HEIGHT = self.maxy - self.miny
        scale_x = self.SCREEN_WIDTH / GEO_WIDTH
        scale_y = self.SCREEN_HEIGHT / GEO_HEIGHT
        self.scale = min(scale_x, scale_y)

    def get_map_bounds(self):
        return self.minx, self.miny, self.maxx, self.maxy

    def get_scale(self):
        return self.scale

    def get_buildings(self):
        building_tags = {"building": True}
        return ox.features_from_polygon(self.area['geometry'].iloc[0], building_tags)