from collections import namedtuple

PointNamedTuple = namedtuple('Point', ['x', 'y'])
point_namedtuple = PointNamedTuple(10, 20)
print(f"Point: {point_namedtuple.x}, {point_namedtuple.y}")