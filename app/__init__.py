from flask import Flask
from .routes import register_routes


def create_app():
    app = Flask(__name__)

    # initialize per‑app state instead of module globals
    app.inventory = []
    app.next_id = 1

    register_routes(app)
    return app