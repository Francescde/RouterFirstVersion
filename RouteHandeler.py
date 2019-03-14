from VehiclesHandeler import vehicles
from MapHandeler import MapHandeler

class RouteHandeler():

    def __init__(self):
        mapHandeler=MapHandeler()
        self.graph = mapHandeler.read_graph("maps/connexioGRAPH2.osm",3007,vehicles)

    def getRoutes(self,lat,lon):
        start = self.graph.getNearestNode(lat, lon)
        ends = [-143102, -170904, -123204, -107948, -81882, -44288, -50156]
        self.graph.solve(start, ends)
        routes = {}
        for end in ends:
            routes[str(end) + "To_Position"] = self.graph.getRoute(end, start, 0)
        return routes

