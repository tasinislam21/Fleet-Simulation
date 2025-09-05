import osmnx as ox
from shapely.geometry import box

class MapGenerator:
    def __init__(self, place_name, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.place_name = place_name
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        place_name = "Hackney, UK" # temp
        self.area_df = ox.geocode_to_gdf(place_name)
        clip_polygon = box(-0.08, 51.545, -0.06, 51.535)
        self.area_df = self.area_df.clip(clip_polygon)
        self.area = self.area_df.geometry.iloc[0]
        self.graph = ox.graph_from_polygon(self.area, network_type="drive")
        self.graph = ox.project_graph(self.graph)
        self.nodes, self.edges = ox.graph_to_gdfs(self.graph, nodes=True, edges=True)

        self.minx, self.miny, self.maxx, self.maxy = self.area_df.total_bounds
        GEO_WIDTH = self.maxx - self.minx
        GEO_HEIGHT = self.maxy - self.miny
        self.scale_x = self.SCREEN_WIDTH / GEO_WIDTH
        self.scale_y = self.SCREEN_HEIGHT / GEO_HEIGHT

    def _normalize_coords(self, x, y):
        norm_x = int((x - self.minx) * self.scale_x)
        norm_y = int(self.SCREEN_HEIGHT - (y - self.miny) * self.scale_y)  # flip Y
        return (norm_x, norm_y)

    def get_map_bounds(self):
        return self.minx, self.miny, self.maxx, self.maxy

    def get_scale(self):
        return self.scale_x, self.scale_y

    def get_buildings_polygon(self):
        building_tags = {"building": True}
        buildings = ox.features_from_polygon(self.area, building_tags)
        buildings = buildings[buildings.geom_type == 'Polygon']
        buildings_coord = []
        for _, building in buildings.iterrows():
            xx, yy = building['geometry'].exterior.coords.xy
            building_coord = []
            for polygon_index in range(len(xx)):
                building_coord.append(self._normalize_coords(xx[polygon_index], yy[polygon_index]))
            buildings_coord.append(building_coord)
        return buildings_coord

    def get_road_line(self):
        road_tags = {"highway": True}
        roads = ox.features_from_polygon(self.area, road_tags)
        roads =  roads[roads.geom_type == 'LineString']
        roads_coord = []
        for _, road in roads.iterrows():
            xx, yy = road['geometry'].coords.xy
            road_coord = []
            for polygon_index in range(len(xx)):
                road_coord.append(self._normalize_coords(xx[polygon_index], yy[polygon_index]))
            roads_coord.append(road_coord)
        return roads_coord

    def get_road_coord(self):
        full_road_coord = []
        road_tags = {"highway": True}
        roads = ox.features_from_polygon(self.area, road_tags)
        roads = roads[roads.geom_type == 'LineString']
        for _, road in roads.iterrows():
            xx, yy = road['geometry'].coords.xy
            for polygon_index in range(len(xx)):
                full_road_coord.append(self._normalize_coords(xx[polygon_index], yy[polygon_index]))
        return full_road_coord
