from flask import Blueprint, request, jsonify
from logger import Logger


class NodeController:
    """
    Controller for handling node-specific execution logic.
    """

    def __init__(self, logger):
        # Initialize the Node Controller with a logger.
        self.logger = logger

    def execute(self, node):
        # Execute the logic of a single node.
        self.logger.log(f"Executing node: {node['id']}", level="info", node_id=node['id'])
        node_type = node.get("type")
        try:
            if node_type == "DataProcessor":
                result = self.process_data(node)
            elif node_type == "ModelTrainer":
                result = self.train_model(node)
            else:
                raise ValueError(f"Unknown node type: {node_type}")
            self.save_result(node, result)
            return result
        except Exception as e:
            self.logger.log(f"Error executing node {node['id']}: {str(e)}", level="error", node_id=node['id'])
            raise

    def process_data(self, node):
        # Simulate processing data in a node.
        self.logger.log(f"Processing data for node {node['id']}", level="info", node_id=node['id'])
        return {"status": "processed", "node_id": node["id"]}

    def train_model(self, node):
        # Simulate training a model.
        self.logger.log(f"Training model for node {node['id']}", level="info", node_id=node['id'])
        return {"status": "trained", "node_id": node["id"]}

    def save_result(self, node, result):
        # Save the execution result of a node.
        self.logger.log(f"Saving result for node {node['id']}: {result}", level="info", node_id=node['id'])


# Flask Blueprint integration
bp = Blueprint("node_controller", __name__, url_prefix="/api/node")

# Initialize logger and NodeController
logger = Logger(module_name="NodeController")
node_controller = NodeController(logger=logger)


@bp.route("/execute", methods=["POST"])
def execute_node():
    """
    API Endpoint: Execute a single node.
    """
    try:
        node = request.json.get("node")
        if not node:
            return jsonify({"error": "node data is required"}), 400
        result = node_controller.execute(node)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        logger.log(f"Error executing node: {str(e)}", level="error")
        return jsonify({"error": str(e)}), 500
