from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from flask_migrate import Migrate
from .authentication.routes import auth
from .api.routes import api


app = Flask(__name__)

CORS(app)
jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(auth)
app.register_blueprint(api)
app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)


if __name__ == '__main__':
    app.debug = True
    app.run()
