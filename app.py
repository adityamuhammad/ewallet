from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_bcrypt import Bcrypt

from database.database_factory import DatabaseFactory
from helper.user_helper import check_password
from services.user_service import UserService

from os import environ



app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTING'))
engine = DatabaseFactory.get()

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def home():
    return {'msg': 'success'}

################# LOGIN ######################
@app.route("/token/auth", methods=['POST'])
def authentication():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = UserService(engine).get_user(email)
    if user:
        check = check_password(user.get('password'), password)
        if check:
            access_token = create_access_token(identity=user.get('id'))
            refresh_token = create_refresh_token(identity=user.get('id'))

            resp = jsonify({'msg': 'login success.'})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
    return jsonify({'msg': 'login failed.'}), 401
    
################# REFRESH TOKEN ######################
@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'msg': 'token refreshed'})
    set_access_cookies(resp, access_token)
    return resp, 200

################# LOGOUT ######################
@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'msg': 'logout success.'})
    unset_jwt_cookies(resp)
    return resp, 200

if __name__ == '__main__':
    app.run()