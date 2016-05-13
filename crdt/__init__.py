from flask import Flask
from counter_api import counter_api_blueprint
from set_api import set_api_blueprint

app = Flask(__name__)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')
app.register_blueprint(set_api_blueprint, url_prefix='/set')


def run():
    app.run()

if __name__ == "__main__":
    run()



