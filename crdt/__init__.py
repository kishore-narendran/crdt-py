from flask import Flask

from crdt.constants import DATA_TYPES, NULL_TYPE, DUMMY_KEY
from crdt.control.client_api import client_api_blueprint
from crdt.control.counter_api import counter_api_blueprint
from crdt.control.set_api import set_api_blueprint
from crdt.control.register_api import register_api_blueprint
from crdt.model.lwwregister import LWWERegister
from redis_manager import redis_manager
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')
app.register_blueprint(set_api_blueprint, url_prefix='/set')
app.register_blueprint(client_api_blueprint, url_prefix='/client')
app.register_blueprint(register_api_blueprint, url_prefix='/register')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


def run():
    # print 'Flush Redis!'
    # redis_manager.flushdb()
    # redis_manager.flushall()
    app.run(debug=True)

if __name__ == "__main__":
    run()
