from flask import Flask,request
from flask_restful import Resource, Api
from flask_restful.utils import cors
from RouteHandeler import RouteHandeler
import json
from flask.views import MethodView
import logging

logging.getLogger('flask_cors').level = logging.DEBUG
app = Flask(__name__)
api = Api(app)

routeHandeler=RouteHandeler()

class calculateRoute(Resource):#Resource

    @cors.crossdomain(origin='*')
    def get(self):
        args = request.args
        print(args)  # For debugging
        lat = args['lat']
        lon = args['lon']
        #start=graph.getNearestNode('41.60448710003', '1.84747999968')
        return json.dumps(routeHandeler.getRoutesWithMandatory(lat,lon,1))


api.add_resource(calculateRoute, '/calculateRoute')
#http://127.0.0.1:5000/calculateRoute?lat=41.60448710003&lon=1.84747999968
if __name__ == '__main__':
    app.run(debug=True)