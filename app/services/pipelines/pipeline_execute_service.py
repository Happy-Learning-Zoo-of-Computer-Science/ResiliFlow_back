import os
import subprocess
import time
import uuid
import threading


class PipelineExecuteService:
    def __init__(self):
        self.exec_result = dict[str, str]()

    def get_execution_status(self, id: str) -> str:
        if id not in self.exec_result:
            return "NOT FOUND"
        return self.exec_result[id]

    def execute_pipeline(self, pipeline_name: str, yaml_path: str) -> str:
        execution_id = uuid.uuid4().hex
        self.exec_result[execution_id] = "PENDING"
        timestamp = int(time.time())
        # create folder if not exists
        os.makedirs("./execution_logs", exist_ok=True)
        output_file = f"./execution_logs/{pipeline_name}-{execution_id}-{timestamp}.log"

        # Open the file in write mode
        def run_subprocess():
            with open(output_file, "w", encoding="utf-8") as file:
                process = subprocess.Popen(
                    [
                        "./act",
                        "-W",
                        yaml_path,
                        "--container-architecture",
                        "linux/amd64",
                    ],
                    stdout=file,  # Redirect stdout to the file
                    stderr=file,  # Redirect stderr to the file
                    text=True,  # Ensure output is written as text, not bytes
                )
                process.wait()
                self.exec_result[execution_id] = "DONE"

        thread = threading.Thread(target=run_subprocess)
        thread.start()

        return execution_id

    def get_execute_logs_by_id(self, pipeline_name, execution_id: str) -> str:
        # get all files in the execution_logs folder
        files = os.listdir("./execution_logs")
        # filter the files with the pipeline_name and execution_id
        filtered_files = [f for f in files if pipeline_name in f and execution_id in f]
        if len(filtered_files) == 0:
            return ""
        # return the first file in the filtered_files
        file_name = filtered_files[0]
        # read the file and return the content
        with open(f"./execution_logs/{file_name}", "r", encoding="utf-8") as f:
            return f.read()

    def get_pipeline_execute_logs_name(self) -> list[dict[str, str]]:
        files = os.listdir("./execution_logs")
        res = []
        # foreach files seperate the pipeline_name and execution_id
        for file in files:
            file_parts = file.split("-")
            pipeline_name = file_parts[0]
            execution_id = file_parts[1]
            timestamp = file_parts[2]
            res.append(
                {
                    "pipeline_name": pipeline_name,
                    "execution_id": execution_id,
                    "timestamp": timestamp,
                    "status": self.exec_result.get(execution_id, "NOT FOUND"),
                }
            )
        return res
