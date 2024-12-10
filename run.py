"""Main function of the project.
"""

from app import create_app
from flask_cors import CORS

app = create_app()
# Allow CORS because Electron is running on a different port.
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

if __name__ == "__main__":
    app.run(debug=True)
