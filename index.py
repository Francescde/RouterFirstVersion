from flask import Flask,request
from flask_restful import Resource, Api
from VehiclesHandeler import vehicles
from MapHandeler import MapHandeler
app = Flask(__name__)
api = Api(app)

mapHandeler=MapHandeler()

graph = mapHandeler.read_graph("maps/connexioGRAPH2.osm",3007,vehicles)

class calculateRoute(Resource):
    def get(self):
        args = request.args
        print(args)  # For debugging
        lat = args['lat']
        lon = args['lon']
        #start=graph.getNearestNode('41.60448710003', '1.84747999968')
        start=graph.getNearestNode(lat, lon)
        ends=[-143102, -170904, -123204, -107948, -81882, -44288, -50156]
        graph.solve(start,ends)
        routes={}
        for end in ends:
            routes[str(end) + "To_Position"] =graph.getRoute(end,start,0)
        return routes


api.add_resource(calculateRoute, '/calculateRoute')
#http://127.0.0.1:5000/calculateRoute?lat=41.60448710003&lon=1.84747999968
if __name__ == '__main__':
    app.run(debug=True)