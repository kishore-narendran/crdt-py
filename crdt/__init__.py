from flask import Flask
from counter_api import counter_api_blueprint
from set_api import set_api_blueprint
from constants import DATA_TYPES, NULL_TYPE, DUMMY_KEY
from redis_manager import redis_manager

app = Flask(__name__)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')
app.register_blueprint(set_api_blueprint, url_prefix='/set')


def run():
    app.run()


def crdt_init():
    redis_manager.hset(DATA_TYPES, DUMMY_KEY, NULL_TYPE)


if __name__ == "__main__":
    crdt_init()
    run()
