import logging
from flask import Blueprint, request, jsonify
from app.services.pipelineMain import PipelineExecutionModuleMain

# 定义 Blueprint，并设置 API 前缀
bp = Blueprint("pipeline_execution", __name__, url_prefix="/api/execution")

# 初始化日志模块
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 PipelineExecutionModuleMain 的实例
pipeline_execution_main = PipelineExecutionModuleMain()


@bp.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    # 接收管道数据并运行整个管道
    try:
        pipeline_data = request.json.get("pipeline_data")
        if not pipeline_data:
            error = 'Missing field "pipeline_data".'
            logger.error(error)
            return jsonify({"error": error}), 400

        result = pipeline_execution_main.execute_pipeline(pipeline_data)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/execute_node", methods=["POST"])
def execute_node():
    # 运行单个节点
    try:
        node = request.json.get("node")
        if not node:
            error = 'Missing field "node".'
            logger.error(error)
            return jsonify({"error": error}), 400

        result = pipeline_execution_main.execute_node(node)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error executing node: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/get_report", methods=["GET"])
def get_report():
    # 获取管道执行报告
    try:
        report_data = pipeline_execution_main.report_generator.get_report_data()
        return jsonify(report_data), 200
    except Exception as e:
        logger.error(f"Error getting report: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/status", methods=["GET"])
def get_status():
    # 检查模块是否运行正常
    return jsonify({"status": "PipelineExecutionModuleMain is running"}), 200
