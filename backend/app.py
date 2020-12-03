from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS

from data_processing.osm_data_processor import OSMDataProcessor
from general_service.service import Service
from graph_constructor.osm_graph_constructor import OsmGraphConstructor

app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)

osm_data_processor = OSMDataProcessor()
constructor = OsmGraphConstructor.create(osm_data_processor, "./cache/", cache=False)
service = Service(constructor)

@api.route('/submit', methods=['POST'])
def handle_submit():
    if request.method == "POST":
        print(request.form, flush=True)

        # do your processing logic here.
        points, paths = service.get_optimal_route(request.form)
        return jsonify(points=points, paths=paths)


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
