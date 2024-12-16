from flask import Blueprint, Flask, jsonify, request
from app.services.pipeline_execution import PipelineExecutionModule
from app.services.NodeController import NodeController
from app.services.ReportGeneration import ReportGenerator
from app.services.logger import Logger

# 初始化蓝图
bp = Blueprint("pipeline_main", __name__, url_prefix="/api/pipeline")


class PipelineExecutionModuleMain:
    """
    主模块：用于初始化和整合管道执行项目中的所有模块。
    """

    def __init__(self):
        # 初始化日志模块
        self.logger = Logger(module_name="PipelineExecutionModuleMain")
        # 初始化报告生成模块
        self.report_generator = ReportGenerator(logger=self.logger)
        # 初始化节点控制模块
        self.node_controller = NodeController(logger=self.logger)
        # 初始化管道执行模块
        self.pipeline_execution = PipelineExecutionModule(
            pipeline_data={}, logger=self.logger
        )
        self.logger.log("PipelineExecutionModuleMain Initialization successful。")

    def execute_pipeline(self, pipeline_data):
        try:
            self.pipeline_execution.pipeline_data = pipeline_data
            self.pipeline_execution.run_pipeline()

            for node_id, result in self.pipeline_execution.execution_context.items():
                self.report_generator.add_node_result(node_id, "success", details=result)

            self.report_generator.finalize_report("success")
            self.logger.log("The pipeline execution completed successfully.")
            return {"status": "success", "execution_context": self.pipeline_execution.execution_context}
        except Exception as e:
            self.logger.log(f"Pipeline execution error: {str(e)}", level="error")
            self.report_generator.finalize_report("failed")
            raise

    def execute_node(self, node):
        try:
            result = self.node_controller.execute(node)
            self.report_generator.add_node_result(node["id"], "success", details=result)
            self.logger.log(f"node {node['id']} Execution Success。")
            return {"status": "success", "result": result}
        except Exception as e:
            self.logger.log(f"node {node['id']} Execution fail: {str(e)}", level="error")
            raise


# 初始化主模块
main_module = PipelineExecutionModuleMain()


# REST API 路由定义
@bp.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    """
    API 端点：运行整个管道。
    """
    try:
        pipeline_data = request.json.get("pipeline_data")
        if not pipeline_data:
            return jsonify({"error": "need pipeline_data"}), 400

        result = main_module.execute_pipeline(pipeline_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/execute_node", methods=["POST"])
def execute_node():
    """
    API 端点：运行单个节点。
    """
    try:
        node = request.json.get("node")
        if not node:
            return jsonify({"error": "Node data required"}), 400

        result = main_module.execute_node(node)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/get_report", methods=["GET"])
def get_report():
    """
    API 端点：获取管道执行报告。
    """
    try:
        report_data = main_module.report_generator.get_report_data()
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 启动 Flask 服务
if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp)  # 注册蓝图
    app.run(host="0.0.0.0", port=8000)
