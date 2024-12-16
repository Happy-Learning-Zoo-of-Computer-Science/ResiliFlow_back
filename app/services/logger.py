import logging
import os
from datetime import datetime


class Logger:
    """
    自定义日志类，支持控制台输出、文件输出，并提供可选的远程日志记录功能。
    """

    def __init__(self, module_name: str, log_file: str = None, remote_logging: bool = False):

        # 初始化 Logger。module_name (str): 日志模块的名称。log_file (str): 日志文件路径。remote_logging (bool): 是否开启远程日志记录。
        self.module_name = module_name
        self.remote_logging = remote_logging
        # 设置日志文件路径，优先从环境变量中获取
        log_file = log_file or os.getenv("LOG_FILE", "pipeline.log")
        # 初始化日志对象
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)  # 设置日志级别
        # 日志格式
        formatter = logging.Formatter(
            "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s"
        )
        # 文件日志处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        # 控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message: str, level: str = "info", **context):

        # 记录日志信息。message (str): 日志内容。level (str): 日志级别，可选值：debug, info, warning, error, critical。**context: 附加的上下文信息。
        log_entry = f"{message} | Context: {context}"
        if level.lower() == "debug":
            self.logger.debug(log_entry)
        elif level.lower() == "warning":
            self.logger.warning(log_entry)
        elif level.lower() == "error":
            self.logger.error(log_entry)
        elif level.lower() == "critical":
            self.logger.critical(log_entry)
        else:
            self.logger.info(log_entry)

        # 可选的远程日志记录
        if self.remote_logging:
            self.send_to_remote_service(log_entry, level)

    def send_to_remote_service(self, log_data, level):
        # 将日志发送到远程服务（占位实现）。
        print(f"Sending to remote service: {log_data} | Level: {level}")
