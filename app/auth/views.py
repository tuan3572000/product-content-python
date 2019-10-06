
from flask import flash, redirect, render_template, url_for, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from . import auth
from ..models import User


@auth.route('/authentication/login', methods=["POST"])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify(error="User doesn't exist"), 401
    if check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(error="Invalid username or password"), 401


