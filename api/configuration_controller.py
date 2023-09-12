from flask import Flask, jsonify

from configurations import get_all_configurations
import repository.configuration_repository as configuration_repository

app = Flask(__name__)


@app.route('/config/<string:config_name>', methods=['GET'])
def get_config(config_name: str):
    if config_name not in get_all_configurations():
        return jsonify({'error': 'No such configuration ' + config_name}), 400

    repository = configuration_repository.get_repository(config_name)
    configurations = repository.get()

    if configurations is None:
        return jsonify({'error': 'Configuration not found'}), 404

    return jsonify(configurations)


if __name__ == '__main__':
    app.run(debug=True)
