import pygame
import geopandas
import osmnx as ox
from shapely.geometry import box
from shapely.geometry import Polygon

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

going_up = False
going_left = False
going_right = False
going_down = False

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working With Rectangles")

place_name = "Hackney, UK"
hackney = ox.geocode_to_gdf(place_name)
polygon = box(-0.1, 51.57, -0.08, 51.56)
poly_gdf = geopandas.GeoDataFrame([1], geometry=[polygon])
hackney_clipped = hackney.clip(polygon)
building_tags = {"building": True}
buildings = ox.features_from_polygon(hackney_clipped['geometry'].iloc[0], building_tags)
buildings = Polygon([(100, 100), (200, 80), (250, 200), (150, 250)])

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            print(f'Mouse position {event.pos}')

    #for _, building in buildings.iterrows():
    #xx, yy = building['geometry'].exterior.coords.xy
    xx, yy = buildings.exterior.coords.xy

    building_coord = []
    for polygon_index in range(len(xx)):
        building_coord.append((xx[polygon_index]+5, yy[polygon_index]+5))
    pygame.draw.polygon(screen, (67, 255, 255), building_coord)

    pygame.display.flip()
    screen.fill((0, 0, 0))

pygame.quit()