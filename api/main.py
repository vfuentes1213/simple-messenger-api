from flask import Flask
from flask_restful import Api
from api.routes import initialize_routes
from api.config.api_config import config
from api.db import db

app = Flask(__name__)
app.config.update(config)
# TODO put prefix in config
api = Api(app, prefix="/api/v1")

initialize_routes(api)


# We only need this in development
@app.before_first_request
def create_tables():
    db.create_all()