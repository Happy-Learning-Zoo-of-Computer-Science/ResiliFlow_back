import json
import datetime
import os
from flask import Blueprint, jsonify, request, current_app
from jinja2 import Template
from app.services.logger import Logger

# 创建 Flask 蓝图
bp = Blueprint("report_generation", __name__, url_prefix="/api/report")


class ReportGenerator:
    # 负责生成管道执行的报告（JSON 和 HTML格式）
    def __init__(self, report_file=None, logger=None):
        self.report_file = report_file or os.getenv("REPORT_FILE", "execution_report.json")
        self.logger = logger or Logger(module_name="ReportGenerator")
        self.report_data = {
            "pipeline_name": None,
            "execution_date": None,
            "nodes": [],
            "overall_status": "Pending",
        }

    def set_pipeline_name(self, pipeline_name):
        self.report_data["pipeline_name"] = pipeline_name
        self.logger.log(f"Pipeline name set to: {pipeline_name}")

    def add_node_result(self, node_id, status, details=None):
        node_report = {
            "node_id": node_id,
            "status": status,
            "details": details or "No details provided.",
        }
        self.report_data["nodes"].append(node_report)
        self.logger.log(f"Node result added: {node_id} - Status: {status}")

    def finalize_report(self, overall_status):
        self.report_data["execution_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report_data["overall_status"] = overall_status
        self._write_to_file()
        self.logger.log(f"Report finalized with status: {overall_status}")

    def _write_to_file(self):
        with open(self.report_file, "w") as file:
            json.dump(self.report_data, file, indent=4)
        self.logger.log(f"Report written to file: {self.report_file}")

    def generate_html_report(self, html_file=None):
        html_file = html_file or os.getenv("HTML_REPORT_FILE", "execution_report.html")
        template = Template("""
        <html>
        <head>
            <title>Pipeline Execution Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #333; }
                ul { list-style-type: none; padding: 0; }
                li { margin-bottom: 10px; border: 1px solid #ccc; padding: 10px; }
            </style>
        </head>
        <body>
            <h1>Pipeline Execution Report</h1>
            <p><strong>Pipeline Name:</strong> {{ pipeline_name }}</p>
            <p><strong>Execution Date:</strong> {{ execution_date }}</p>
            <p><strong>Overall Status:</strong> {{ overall_status }}</p>
            <h2>Node Execution Details:</h2>
            <ul>
            {% for node in nodes %}
                <li>
                    <strong>Node ID:</strong> {{ node.node_id }}<br>
                    <strong>Status:</strong> {{ node.status }}<br>
                    <strong>Details:</strong> {{ node.details }}
                </li>
            {% endfor %}
            </ul>
        </body>
        </html>
        """)
        html_content = template.render(
            pipeline_name=self.report_data["pipeline_name"],
            execution_date=self.report_data["execution_date"],
            overall_status=self.report_data["overall_status"],
            nodes=self.report_data["nodes"]
        )
        with open(html_file, "w") as file:
            file.write(html_content)
        self.logger.log(f"HTML report generated at: {html_file}")

    def get_report_data(self):
        return self.report_data


# 实例化 ReportGenerator
report_generator = ReportGenerator(logger=Logger(module_name="ReportGenerator"))


# REST API 路由
@bp.route("/finalize", methods=["POST"])
def finalize_report():
    """
    终结报告并保存为 JSON 文件。
    """
    try:
        data = request.get_json()
        overall_status = data.get("overall_status", "Pending")
        report_generator.finalize_report(overall_status)
        return jsonify({"message": "Report finalized successfully"}), 200
    except Exception as e:
        report_generator.logger.log(f"Error finalizing report: {str(e)}", level="error")
        return jsonify({"error": str(e)}), 500


@bp.route("/data", methods=["GET"])
def get_report():
    """
    获取当前的报告数据。
    """
    try:
        return jsonify(report_generator.get_report_data()), 200
    except Exception as e:
        report_generator.logger.log(f"Error fetching report: {str(e)}", level="error")
        return jsonify({"error": str(e)}), 500


@bp.route("/html", methods=["POST"])
def generate_html():
    """
    生成 HTML 格式的报告。
    """
    try:
        html_file = current_app.config.get("HTML_REPORT_FILE", "execution_report.html")
        report_generator.generate_html_report(html_file)
        return jsonify({"message": f"HTML report generated at {html_file}"}), 200
    except Exception as e:
        report_generator.logger.log(f"Error generating HTML report: {str(e)}", level="error")
        return jsonify({"error": str(e)}), 500
