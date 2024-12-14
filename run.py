"""Main function of the project.
"""

from flask_cors import CORS

from app import create_app


app = create_app()


# Allow CORS because Electron is running on a different port.
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

if __name__ == "__main__":
    app.run(debug=True)
