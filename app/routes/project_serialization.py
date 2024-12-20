"""A blue print of /api/project
"""

import logging

from flask import Blueprint, jsonify, request, Response

from app.services.project_serialization import ProjectSerializor

bp = Blueprint("project", __name__, url_prefix="/api/project")


@bp.route("/languages", methods=["GET"])
def get_supported_languages() -> Response:
    """Get supported languages.

    Returns:
        Response: [languages].
    """
    return jsonify(ProjectSerializor.get_supported_langauges())


@bp.route("/frameworks", methods=["GET"])
def get_supported_frameworks() -> Response:
    """Get supported frameworks of a language.

    Returns:
        Response: [frameworks].
    """

    language = request.args.get("language")
    if language is None:
        error = 'Missing field "language".'
        logging.error(error)
        return jsonify({"error": error}), 400
    result = ProjectSerializor.get_supported_frameworks(language)
    return jsonify(result)


@bp.route("/configurations/supported", methods=["GET"])
def get_supported_configurations() -> Response:
    """Get supported configurations of a language and a framework.

    Returns:
        Response: {configuration: attributes}, 400 (Missing field), 415 (No payload)
    """

    language = request.args.get("language")
    if language is None:
        error = 'Missing field "language".'
        logging.error(error)
        return jsonify({"error": error}), 400

    framework = request.args.get("framework", None)
    result = ProjectSerializor.get_configurations(language, framework)
    return jsonify(result)


@bp.route("/configurations/initialized", methods=["GET"])
def get_initialized_configurations() -> Response:
    """Get initialized configurations of a language and a framework in a path.

    Returns:
        Response: [configuration files name], 400 (Missing field, path doesn't exist), 415 (No payload)
    """

    path = request.args.get("path")
    language = request.args.get("language")
    if language is None:
        error = 'Missing field "language".'
        logging.error(error)
        return jsonify({"error": error}), 400
    if path is None:
        error = 'Missing field "path".'
        logging.error(error)
        return jsonify({"error": error}), 400


    framework = request.args.get("framework", None)

    try:
        result = ProjectSerializor.get_initialized_configurations(
            path, language, framework
        )
        return jsonify(result)
    except NotADirectoryError as ex:
        return jsonify({"error": ex.args[0]}), 400


@bp.route("/validate", methods=["GET"])
def is_project_initialized() -> Response:
    """Check is a project initialized.

    Returns:
        Response: {"valid": T | F}, 400 (Missing field), 415 (No payload)
    """

    path = request.args.get("path")
    if path is None:
        error = 'Missing field "path".'
        logging.error(error)
        return jsonify({"error": error}), 400

    try:
        result = ProjectSerializor.is_initialized(path)
        return jsonify({"valid": result})
    except NotADirectoryError:
        return jsonify({"error": "Path doesn't exist."}), 400


@bp.route("/create", methods=["POST"])
def create_project() -> Response:
    """Call create_project service.

    Returns:
        Response: 200, 400 (Missing fields, path doesn't exist), 500 (Unknown)
    """

    # Get attributes.
    data: dict = request.get_json()
    try:
        ProjectSerializor.create_project(data)
        return "", 200
    except (KeyError, ValueError, NotADirectoryError) as ex:
        return jsonify({"error": ex.args[0]}), 400
