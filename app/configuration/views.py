from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Configuration
from . import configuration


@configuration.route("/admin/configuration", methods=['POST'])
@jwt_required
def save_all_configurations():
    data = request.get_json()
    configs_data = data['configurations']
    for config_data in configs_data:
        config = Configuration()
        config.key = config_data['key']
        config.value = config_data['value']
        db.session.add(config)
    db.session.commit()
    return jsonify(configs_data), 201


@configuration.route("/admin/configuration/contact-us")
def get_contactUs_configs():
    configs = Configuration.query.filter(
        Configuration.key in ["location-image", "address", "email", "facebook", "phone", "twitter"]).all()
    return jsonify(configs), 200


@configuration.route("/admin/configuration/all")
def get_all_configs():
    configs = Configuration.query.all()
    return jsonify(configs), 200


@configuration.route("/admin/configuration/about-us")
def get_aboutUs_configs():
    configs = Configuration.query.filter(
        Configuration.key in ["location-image", "address", "email", "facebook", "phone", "twitter"]).all()
    return jsonify(configs), 200
