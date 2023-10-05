from flask import Flask, jsonify

import repository.configuration as configuration_repository
from configurations import get_all_configurations, ConfigurationId

app = Flask(__name__)


@app.route('/config/<string:config_name>', methods=['GET'])
def get_config(config_name: ConfigurationId):
    if config_name not in get_all_configurations():
        return jsonify({'error': 'No such configuration ' + config_name}), 400

    repository = configuration_repository.get_repository(config_name)
    configurations = repository.get()

    return jsonify([c.as_dict() for c in configurations])


if __name__ == '__main__':
    app.run(debug=True)
