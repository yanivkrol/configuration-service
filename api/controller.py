from flask import Flask, Blueprint, jsonify

import model.configuration as configuration_models
import response
from app.middleware.database_interface import DatabaseInterface
from configurations import get_all_configurations, ConfigurationId
from db_config import SessionMaker

api_v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


@api_v1.route('/config/<string:config_id>', methods=['GET'])
def get_config(config_id: ConfigurationId):
    if config_id not in get_all_configurations():
        return jsonify({'error': 'No such configuration ' + config_id}), 400

    session = SessionMaker()
    c_model = configuration_models.get_model(config_id)
    configurations = DatabaseInterface(c_model, session).get_all()

    c_response = response.get_response(config_id)
    items = []
    for c in configurations:
        items.append({
            'key': c_response.get_key(c),
            'data': c_response.get_data(c),
            'active': c.active,
        })

    return jsonify(items)


app = Flask(__name__)
app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(debug=True)
