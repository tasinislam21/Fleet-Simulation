from pygame import Rect

r = Rect(1, 1, 10, 10)

rects = [
    Rect(1, 1, 10, 10),
    Rect(5, 5, 10, 10),
    Rect(15, 15, 1, 1),
    Rect(2, 2, 1, 1),
]

result = r.collideobjects(rects)  # -> <rect(1, 1, 10, 10)>
print(result)

# front_car = self.check_front_vehicle(vehicles)

# if front_car:
#     # slow down to zero when too close
#     distance = (front_car.pos - self.pos).length()
#     if distance < 40:
#         self.vel *= 0.5  # reduce speed
#     if distance < 20:
#         self.vel *= 0  # full stop

def check_front_vehicle(self, vehicles, safe_distance=40):
    for other in vehicles:
        if other is self:
            continue

        offset = other.current_position - self.current_position
        # Is the other car roughly in front of me?
        if self.vel.length_squared() > 0:
            forward = self.vel.normalize()
            if forward.dot(offset.normalize()) > 0.7:  # ~within 45° cone ahead
                if offset.length() < safe_distance:
                    return other
    return None