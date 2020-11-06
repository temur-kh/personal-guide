from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from general_service.serivce import get_optimal_route


app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)


@api.route('/submit', methods=['POST'])
def handle_submit():
    if request.method == "POST":
        print(request.form, flush=True)

        # do your processing logic here.
        # return jsonify(service.get_optimal_route(request.form))
        return jsonify(request.form)


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
