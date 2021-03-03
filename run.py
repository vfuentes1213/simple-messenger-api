# api entry point
import os

from api.main import app

FLASK_DEBUG = bool(os.environ.get("FLASK_DEBUG", False))

if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)