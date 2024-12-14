"""Create a Flask app and connect routes.
"""


from flask import Flask

from app.routes import pipeline_execute_blueprint, project_serialization


def create_app() -> Flask:
    """Create a Flask app and connect routes.

    Returns:
        Flask: A Flask app.
    """

    app = Flask(__name__)
    app.register_blueprint(project_serialization.bp)
    app.register_blueprint(pipeline_execute_blueprint.pipeline_blueprint())
    return app
