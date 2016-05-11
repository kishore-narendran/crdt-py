from flask import Flask
from counter_api import counter_api_blueprint

app = Flask(__name__)

app.register_blueprint(counter_api_blueprint, url_prefix='/counter')

if __name__ == "__main__":
    app.run()
