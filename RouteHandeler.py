from VehiclesHandeler import vehicles
from MapHandeler import MapHandeler

def min_route_walking(routes):
    minWalking=99999
    routeS=[]
    pos=0
    cost0=99999
    for key, route in routes.items():
        i=0
        #print(route[i])
        while(i<len(route) and route[i]['vehicle']!='walk'):
            i=i+1
        if(i<len(route)):
            if route[i]['cost']<=minWalking:
                if route[i]['cost']==minWalking:
                    if(cost0>route[0]['cost']):
                        minWalking=route[i]['cost']
                        routeS=route
                        pos=i
                        cost0 = route[0]['cost']
                else:
                    minWalking=route[i]['cost']
                    routeS=route
                    pos=i
                    cost0 = route[0]['cost']
        else:
            if route[i-1]['cost']<=minWalking:
                if route[i-1]['cost']==minWalking:
                    if(cost0>route[0]['cost']):
                        minWalking=route[i-1]['cost']
                        routeS=route
                        pos=i-1
                        cost0 = route[0]['cost']
                else:
                    minWalking=route[i-1]['cost']
                    routeS=route
                    pos=i-1
                    cost0 = route[0]['cost']
    return routeS, pos, minWalking, routeS[0]['point']

def min_route(routes):
    routeS=[]
    cost0=9999999
    for key, route in routes.items():
        if (cost0 > route[0]['cost']):
            routeS = route
            cost0 = route[0]['cost']
    i=0
    while(i<len(route) and route[i]['vehicle']!='walk'):
        i=i+1
    pos=i-1
    minWalking = route[pos]['cost']
    return routeS, pos, minWalking, routeS[0]['point']

class RouteHandeler():

    def __init__(self):
        mapHandeler=MapHandeler()
        self.graphMultimodal, self.graphUnimodal = mapHandeler.read_graph("maps/connexioGRAPH2.osm",3007,vehicles)

    def getRoutes(self,lat,lon):
        start = self.graphMultimodal.getNearestNode(lat, lon)
        #-123204
        ends = [-131168, -102262, -124744, -157746]#[-143102, -170904, -107948, -81882, -44288, -50156,-123204]
        self.graphMultimodal.solve(start, ends)
        routes = {}
        for end in ends:
            routes[str(end) + "To_Position"] = self.graphMultimodal.getRoute(end, start, 1)
        return routes

    def findMaxPosForVehicle(self,route,pos,vehicle):
        i=1
        while(i<=pos and i<len(route) and self.graphMultimodal.findVehicleCanGoToPred(route[i]['point'],vehicle)):
            i=i+1
        if(i==len(route)):
            i=i-1
        return i

    def getRoutesWithMandatory(self,lat,lon,vehicle):
        start = self.graphMultimodal.getNearestNode(lat, lon)
        #-123204
        ends = [-131168, -102262, -124744, -157746]#[-143102, -170904, -107948, -81882, -44288, -50156,-123204]
        self.graphMultimodal.solve(start, ends)
        routes = {}
        for end in ends:
            routes[str(end) + "To_Position"] = self.graphMultimodal.getRoute(end, start)
        #print(start)
        #print(routes)
        route, pos, minWalkDsit, point = min_route(routes)#min_route_walking(routes)

        routeSel={}
        routeSel[str(point) + "To_Position"] = route
        if pos>0:
            print('-----')
            print(route)
            print('maxPos '+str(pos))
            pos2 = self.findMaxPosForVehicle(route,pos,vehicle)
            print(pos2)
            print(pos)
            print(route[pos2]['point'])
            print('solve')
            self.graphUnimodal.solve(route[pos2]['point'], vehicle)

            vehiclesSTR=['walk','car','BRP','4x4']
            route[pos2]['limitVehicle']=vehiclesSTR[vehicle]
            #print(route[pos2])
            #print('solve2')
            routes2 = {}
            route2min=[]
            route2dist=999999
            for end in ends:
                routes2[str(end) + "To_Position"] = self.graphUnimodal.getRoute(end, route[pos2]['point'], vehicle)
                R2dist=routes2[str(end) + "To_Position"][0]['cost']
                if(R2dist<route2dist):
                    #print(R2dist)
                    route2dist=R2dist
                    route2min=routes2[str(end) + "To_Position"]
            ##print(routes2)
            if(len(route2min)>0):
                routeSel["car"+str(point) + "To_Position"] = route2min
        return routeSel

