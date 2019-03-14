from router.router import routerc
import xml.etree.ElementTree as ET


INF=99999


def walkingCost( distance, positiveRmp, negativeRmp, type, footSpeeds):
    if (type['type'] == "track"):
        tracktype = type["tracktype"]
        speed = str(footSpeeds[type['type']][tracktype])
    else:
        speed = str(footSpeeds[type['type']])
    if speed =='inf':
        return INF
    speed=float(speed)/3.6
    cost = distance / speed
    inclinationpos = positiveRmp / distance
    inclinationneg = -negativeRmp / distance
    cost = cost * (1 + inclinationpos) * (1 + (inclinationneg / 3))
    return cost


def vehicleCost( distance, type, oneway, vehicle):
    if oneway:
        cost = INF
    else:
        if (type['type'] == "track"):
            tracktype = type["tracktype"]
            speed = str(vehicle[type['type']][tracktype])
        else:
            speed = str(vehicle[type['type']])
        if speed =='inf':
            return INF
        speed=float(speed)/3.6
        cost = distance / speed
    return cost

class MapHandeler():

    def read_graph(self,filename,numNodes,vehicles):
        graph=routerc(numNodes)
        tree = ET.parse(filename)
        root = tree.getroot()

        tree_points=root.iter("node")
        tree_paths=root.iter("way")
        for i in tree_points:
            n=i.attrib
            nodeKey=int(n["id"])
            graph.addNode(nodeKey,str(n["lat"]),str(n['lon']))
        for i in tree_paths:
            points = []
            for point in i.iter("nd"):
                points.append(int(point.attrib["ref"]))
            distanceTo=INF
            distanceFrom=INF
            oneway=0
            positiveRmp=0
            negativeRmp=0
            type={'type':"path",
                  "tracktype":"grade1"}
            for tags in i.iter("tag"):
                #Distance_From_-141878_To_-110796
                if(str(tags.attrib["k"])=="Distance_From_"+str(points[0])+"_To_"+str(points[1]) ):
                    distance=float(tags.attrib["v"])
                    #graph.inicializeEdge(points[0],points[1],distance)
                    distanceTo=distance
                if(str(tags.attrib["k"])=="Distance_From_"+str(points[1])+"_To_"+str(points[0]) ):
                    distance=float(tags.attrib["v"])
                    #graph.inicializeEdge(points[1],points[0],distance)
                    distanceFrom=distance
                if(str(tags.attrib["k"])=="oneway" ):
                    if(tags.attrib["v"]=="yes"):
                        oneway=1
                    else:
                        oneway=-1
                if(str(tags.attrib["k"])=="highway" ):
                    type['type']=tags.attrib["v"]
                if(str(tags.attrib["k"])=="tracktype" ):
                    type['tracktype']=tags.attrib["v"]
                if(str(tags.attrib["k"])=="Positive Ramp" ):
                    positiveRmp=float(tags.attrib["v"])
                if(str(tags.attrib["k"])=="Negative Ramp" ):
                    negativeRmp=float(tags.attrib["v"])
            #['Car', '4x4', 'BRP', 'Foot']
            if distanceTo > 0:
                walkingCost1=walkingCost(distanceTo,positiveRmp,negativeRmp,type,vehicles['Foot'])
                CarCost1=vehicleCost(distanceTo,type,oneway==1,vehicles['Car'])
                BRPCost1=vehicleCost(distanceTo,type,oneway==1,vehicles['BRP'])
                AllTerrainCost1=vehicleCost(distanceTo,type,oneway==1,vehicles['4x4'])
                #print(str(points[0])+" "+str(points[1])+" "+str(walkingCost1)+" "+str(CarCost1)+" "+str(BRPCost1)+" "+str(AllTerrainCost1))
                graph.inicializeEdge(points[1], points[0], walkingCost1,CarCost1,BRPCost1,AllTerrainCost1,positiveRmp,negativeRmp,distanceTo)
            if distanceFrom > 0:
                walkingCost2=walkingCost(distanceFrom,negativeRmp*-1,positiveRmp*-1,type,vehicles['Foot'])
                CarCost2=vehicleCost(distanceFrom,type,oneway==-1,vehicles['Car'])
                BRPCost2=vehicleCost(distanceFrom,type,oneway==-1,vehicles['BRP'])
                AllTerrainCost2=vehicleCost(distanceFrom,type,oneway==-1,vehicles['4x4'])
                #print(str(points[1])+" "+str(points[0])+" "+str(walkingCost2)+" "+str(CarCost2)+" "+str(BRPCost2)+" "+str(AllTerrainCost2))
                graph.inicializeEdge(points[0], points[1], walkingCost2,CarCost2,BRPCost2,AllTerrainCost2,positiveRmp,negativeRmp,distanceFrom)

        #DataFile = open("pointData.json", "w")
        #DataFile.write(simplejson.dumps(graph.returnNodes(), indent=4, sort_keys=True))
        #DataFile.close()
        return graph
