from flask import Blueprint, jsonify, request, Response
from marshmallow import ValidationError


from app.requests.pipeline_execute_request import PipelineExecuteRequest
from app.services.pipelines.pipeline_execute_service import PipelineExecuteService


def pipeline_blueprint() -> Blueprint:
    bp = Blueprint("pipeline", __name__, url_prefix="/api/pipeline")
    service = PipelineExecuteService()

    @bp.route("/execute", methods=["POST"])
    def execute_pipeline() -> tuple[Response, int]:
        """ """
        request_data = request.json
        if request_data is None:
            return (jsonify({"error": "Invalid request data"}), 400)

        schema = PipelineExecuteRequest()
        try:
            # Validate request body against schema data types
            result = schema.load(request_data)
        except ValidationError as err:
            # Return a nice message if validation fails
            return (jsonify({"error": err.messages}), 400)
        result = service.execute_pipeline(result["pipeline_name"], result["yaml_path"])
        return (jsonify({"result": result}), 200)

    @bp.route("/execute_result/<id>", methods=["Get"])
    def get_execution_status(id: str) -> tuple[Response, int]:
        return (
            jsonify({"status": service.get_execution_status(id)}),
            200,
        )

    return bp
