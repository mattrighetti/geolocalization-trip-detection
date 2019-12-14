from shapely.geometry import Point
from Utils import stops

if __name__ == '__main__':
    # I am instantiating the stop object
    s = stops.stops()
    # Creating the two points:
    # Starting point p1
    # Ending point p2
    p1 = Point(9.176254158417308, 45.467950018575024)
    p2 = Point(9.214046555959797, 45.48934886764579)
    # Loooking for the bus stops close to the start point
    Ilist = s.find_bus_stops_close_to(p1, radius=0.0005)
    # Loooking for the bus stops close to the ending point
    Flist = s.find_bus_stops_close_to(p2, radius=0.0005)
    # Filtering the buses that are not in common in the two sets
    Ilist, Flist = stops.intercept(Ilist, Flist)

    print("ILIST")
    print(type(Ilist))
    print(Ilist)
    print("FLIST")
    print(type(Flist))
    print(Flist)