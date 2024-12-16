"""Main function of the project.
"""

import argparse

from app import create_app
from flask_cors import CORS

app = create_app()
# Allow CORS because Electron is running on a different port.
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Use debug mode or not.
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Use debug mode")

if __name__ == "__main__":
    args = parser.parse_args()
    app.run(debug=args.debug)
