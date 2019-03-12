import unittest
import os
os.chdir('..')
from MapHandeler import MapHandeler


def getGraphKeys( graph, end, start):
    route = [end]
    key, j = graph.findPredecesor(graph.getKey(end))
    route.append(j)
    while j != start:
        key, j = graph.findPredecesor(key)
        route.append(j)
    return route

class TestStringMethods(unittest.TestCase):

    def test_readGraff(self):
        from Tests.FakesVehicles.FakeVehicles import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("maps/connexioGRAPH2.osm", 3007, vehicles)
        self.assertTrue(True)

    def test_if_sum_larger_than_direct_root_take_sum_of_nodes(self):
        from Tests.FakesVehicles.FakeVehiclesJustWalking import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("Tests/maps/simpleGraf.osm", 7, vehicles)
        start = -26176
        ends = [-26182, -29888]
        graph.solve(start, ends)
        k=0
        for end in ends:
            route = getGraphKeys(graph,end,start)
            if k==0:
                self.assertEqual([end,-26181,-26180,-26179,-26178,start],route)
            else:
                self.assertEqual([end,start],route)
            k=k+1

    def test_if_sum_larger_than_direct_root_take_direct_root(self):
        from Tests.FakesVehicles.FakeVehiclesJustWalking import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("Tests/maps/simpleGraf2.osm", 7, vehicles)
        start = -26176
        ends = [-26182, -29888]
        graph.solve(start, ends)
        k=0
        for end in ends:
            route = getGraphKeys(graph,end,start)
            if k==0:
                self.assertEqual([end,-26179,-26178,start],route)
            else:
                self.assertEqual([end,start],route)
            k=k+1

    def test_if_route_car_is_better_take_car(self):
        from Tests.FakesVehicles.FakeVehicles import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("Tests/maps/simpleGraf3.osm", 7, vehicles)
        start = -26176
        ends = [-26182, -29888]
        graph.solve(start, ends)
        k=0
        for end in ends:
            route = getGraphKeys(graph,end,start)
            if k==0:
                self.assertEqual([end,-26181,-26180,-26179,-26178,start],route)
            else:
                self.assertEqual([end,start],route)
            k=k+1



    def test_if_route_walk_is_better_walk(self):
        from Tests.FakesVehicles.FakeVehicles import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("Tests/maps/simpleGraf4.osm", 7, vehicles)
        start = -26176
        ends = [-26182, -29888]
        graph.solve(start, ends)
        k=0
        for end in ends:
            route = getGraphKeys(graph,end,start)
            if k==0:
                self.assertEqual([end,start],route)
            else:
                self.assertEqual([end,start],route)
            k=k+1


    def test_if_you_leaveTheCar_you_cant_take_it_again(self):
        from Tests.FakesVehicles.FakeVehicles import vehicles
        mapHandeler=MapHandeler()
        graph = mapHandeler.read_graph("Tests/maps/simpleGraf5.osm", 7, vehicles)
        start = -26176
        ends = [-26182]
        graph.solve(start, ends)
        route = getGraphKeys(graph,ends[0],start)
        self.assertEqual([ends[0],-26181,-26180,-26179,-26178,start],route)



if __name__ == '__main__':
    unittest.main()