from flask import Flask

from crdt.constants import DATA_TYPES, NULL_TYPE, DUMMY_KEY
from crdt.control.client_api import client_api_blueprint
from crdt.control.counter_api import counter_api_blueprint
from crdt.control.set_api import set_api_blueprint
from crdt.model.pnset import PNSet
from redis_manager import redis_manager

app = Flask(__name__)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')
app.register_blueprint(set_api_blueprint, url_prefix='/set')
app.register_blueprint(client_api_blueprint, url_prefix='/client')


def run():
    # print 'Flush Redis!'
    # redis_manager.flushdb()
    # redis_manager.flushall()
    app.run(debug=True)

if __name__ == "__main__":
    run()
