
class DrivableRoad(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DrivableRoad, cls).__new__(cls)
        return cls.instance

    def set_drivable_road(self, full_road_coord):
        self.full_road_coord = full_road_coord

    def get_drivable_road(self):
        return self.full_road_coord