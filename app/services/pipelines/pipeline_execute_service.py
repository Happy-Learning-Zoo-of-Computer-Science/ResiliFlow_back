import subprocess
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
        id = uuid.uuid4().hex
        self.exec_result[id] = "PENDING"
        output_file = f"./pipeline-{id}.log"

        # Open the file in write mode
        def run_subprocess():
            with open(output_file, "w", encoding="utf-8") as file:
                process = subprocess.Popen(
                    [
                        "./act",
                        "-W",
                        ".github/workflows/test-on-pr.yml",
                        "--container-architecture",
                        "linux/amd64",
                    ],
                    stdout=file,  # Redirect stdout to the file
                    stderr=file,  # Redirect stderr to the file
                    text=True,  # Ensure output is written as text, not bytes
                )
                process.wait()
                self.exec_result[id] = "DONE"

        thread = threading.Thread(target=run_subprocess)
        thread.start()

        return id
