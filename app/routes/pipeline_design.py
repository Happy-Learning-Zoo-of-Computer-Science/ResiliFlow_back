from flask import Blueprint, jsonify, request, Response

from app.services.nodeData import deserialize, compile

bp = Blueprint("pipeline_design", __name__, url_prefix="/api/pipeline")


@bp.route("/compile", methods=["GET"])
def get_supported_languages() -> Response:
    nodes=deserialize()
    file_path=compile(nodes)

    return jsonify(file_path)