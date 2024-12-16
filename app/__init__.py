"""Create a Flask app and connect routes.
"""

from flask import Flask

from app.routes import project_serialization
from app.routes import pipeline_design


def create_app() -> Flask:
    """Create a Flask app and connect routes.

    Returns:
        Flask: A Flask app.
    """

    app = Flask(__name__)
    app.register_blueprint(project_serialization.bp)
    app.register_blueprint(pipeline_design.bp)

    return app
