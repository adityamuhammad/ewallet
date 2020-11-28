from flask import Flask, jsonify, request

from database.database_factory import DatabaseFactory

from os import environ



app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTING'))
engine = DatabaseFactory.get()


@app.route('/', methods=['GET'])
def home():
    return {'msg': 'success'}

if __name__ == '__main__':
    app.run()