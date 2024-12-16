import logging
from flask import Blueprint, jsonify, request, Response
from app.services.nodeData import deserialize, compile

bp = Blueprint("pipeline_design", __name__, url_prefix="/api/pipeline")


@bp.route("/compile", methods=["GET"])
def call_compile() -> Response:
    payload = request.args
    print(payload["input"], payload["output"])
    if "input" not in payload:
        error = 'Missing field "input".'
        logging.error(error)
        return jsonify({"error": error}), 400
    if "output" not in payload:
        error = 'Missing field "output".'
        logging.error(error)
        return jsonify({"error": error}), 400
    nodes = deserialize(payload["input"])
    file_path = compile(payload["output"], nodes)

    return jsonify(file_path)