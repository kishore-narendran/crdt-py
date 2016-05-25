from flask import Flask

from crdt.constants import DATA_TYPES, NULL_TYPE, DUMMY_KEY
from crdt.control.counter_api import counter_api_blueprint
from crdt.control.set_api import set_api_blueprint
from crdt.control.client_api import client_api_blueprint
from redis_manager import redis_manager
from crdt.model.pncounter import PNCounter

app = Flask(__name__)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')
app.register_blueprint(set_api_blueprint, url_prefix='/set')
app.register_blueprint(client_api_blueprint, url_prefix='/client')


def run():
    # print 'Flush Redis!'
    # redis_manager.flushdb()
    # redis_manager.flushall()
    gc = PNCounter(key='abcd')
    gc.add_client('a')
    gc.set('a', 5, 0)
    gc.add_client('b')
    gc.set('b', 2, 1)
    gc.add_client('c')
    gc.set('c', 3, 2)
    gc.add_client('d')
    gc.set('d', 4, 4)

    print gc.get('d')
    app.run(debug=True)

if __name__ == "__main__":
    run()
