from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_bcrypt import Bcrypt
from cerberus import Validator

from database.database_factory import DatabaseFactory
from helper.user_helper import check_password
from services.user_service import UserService
from services.wallet_service import WalletService
from os import environ
from helper.enums import Transaction_Type
from validation_schema.user_topup_validation import user_topup_validation_schema
from validation_schema.bank_transfer_validation import bank_transfer_validation_schema



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
    user = UserService(engine).get_user_by_email(email)
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
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'msg': 'token refreshed'})
    set_access_cookies(resp, access_token)
    return resp, 200

################# LOGOUT ######################
@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'msg': 'logout success.'})
    unset_jwt_cookies(resp)
    return resp, 200

################# TOPUP ######################
@app.route('/api/topup', methods=['POST'])
@jwt_required
def topup():
    user_id = get_jwt_identity()
    user = UserService(engine).get_user_by_id(user_id)

    data = {
        'amount': request.json.get('amount', None),
        'user_agent': request.headers.get('User-Agent'),
        'ip': request.headers.get('ip-address'),
        'location': request.headers.get('location'),
        'type': Transaction_Type.DEBIT,
        'author': user.get('username'),
        'user_id': user_id
    }
    v = Validator(user_topup_validation_schema)
    if v.validate(data):
        WalletService(engine, data).topup()
        return {"msg": "transaction success."}, 200
    return {"msg": "validation error, transaction failed.", "errors": v.errors}, 400

################# TRANSFER ######################
@app.route('/api/transfer', methods=['POST'])
@jwt_required
def transfer():
    user_id = get_jwt_identity()
    user = UserService(engine).get_user_by_id(user_id)

    data = {
        'amount': request.json.get('amount', None),
        'code': request.json.get('code', None),
        'user_agent': request.headers.get('User-Agent'),
        'ip': request.headers.get('ip-address'),
        'location': request.headers.get('location'),
        'author': user.get('username'),
        'user_id': user_id
    }
    v = Validator(bank_transfer_validation_schema)
    if v.validate(data):
        wallet_service = WalletService(engine, data)
        if wallet_service.check_balance():
            wallet_service.transfer()
            return {"msg": "transaction success."}, 200
        else:
            return {"msg": "user balance is not sufficient, transaction failed."}, 400
    return {"msg": "validation error, transaction failed.", "errors": v.errors }, 400

if __name__ == '__main__':
    app.run()