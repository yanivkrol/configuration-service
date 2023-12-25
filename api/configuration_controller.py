from flask import Flask, jsonify

import repository.configuration as configuration_repository
from configurations import get_all_configurations, ConfigurationId

app = Flask(__name__)


@app.route('/api/v1/config/<string:config_name>', methods=['GET'])
def get_config(config_name: ConfigurationId):
    if config_name not in get_all_configurations():
        return jsonify({'error': 'No such configuration ' + config_name}), 400

    repository = configuration_repository.get_repository(config_name)
    configurations = repository.get()

    items = []
    for c in configurations:
        key = c.as_dict()
        active = key.pop('active')
        items.append({
            'key': key,
            'active': active,
            'data': None
        })

    return jsonify(items)


if __name__ == '__main__':
    app.run(debug=True)
