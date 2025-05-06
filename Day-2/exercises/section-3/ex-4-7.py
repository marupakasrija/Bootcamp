from collections import namedtuple

InvalidPointNamedTuple = namedtuple('Point', ['x', '1y'])
invalid_point_namedtuple = InvalidPointNamedTuple(5, 15)
print(f"Invalid Point (renamed fields): {invalid_point_namedtuple._0}, {invalid_point_namedtuple._1}")
