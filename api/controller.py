from enum import Enum

from flask import Flask, Blueprint, jsonify

import common.model.configuration as configuration_models
from common.configurations import get_all_configurations, ConfigurationId
from common.database_interface import DatabaseInterface
from common.db_config import SessionMaker

api_v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


def enums_as_names(dictionary: dict) -> None:
    """
    Converts all enums in the dictionary to their names.
    For example, if the enum is defined as AN_ENUM = "An Enum" then the value will be "AN_ENUM".
    """
    for k, v in dictionary.items():
        if isinstance(v, Enum):
            dictionary[k] = v.name


@api_v1.route('/config/<string:config_id>', methods=['GET'])
def get_config(config_id: ConfigurationId):
    if config_id not in get_all_configurations():
        return jsonify({'error': 'No such configuration ' + config_id}), 400

    session = SessionMaker()
    c_model = configuration_models.get_model(config_id)
    configurations = DatabaseInterface(c_model, session).get_all()
    configurations_as_dicts = [c.as_dict() for c in configurations]
    for c in configurations_as_dicts:
        enums_as_names(c)
    return jsonify(configurations_as_dicts)


app = Flask(__name__)
app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(debug=True)
