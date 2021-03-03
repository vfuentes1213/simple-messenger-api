# api entry point
import os

from api.main import app
from api.db import db

FLASK_DEBUG = bool(os.environ.get("FLASK_DEBUG", False))

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=FLASK_DEBUG)