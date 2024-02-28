import datetime
import logging
import os
import sys
import warnings
from typing import TextIO

import wandb


def get_logger(
    name: str,
    log_dir: str,
    log_name: str = "run.log",
    log_format: str = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S'",
    level: int = logging.INFO,
):
    """对 logger 进行一些初始化"""
    logger = logging.getLogger(name)
    file_path = os.path.join(log_dir, log_name)
    hdlr = logging.FileHandler(file_path)
    formatter = logging.Formatter(log_format)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger


def wandb_log_histogram(
    key,
    values,
    step=None,
    commit=True,
    sync=True,
):
    """封装一下 wandb 的 API，不要直接暴露 wandb 实例"""
    wandb.log({key: values}, step=step, commit=commit, sync=sync)


class DualOutput(TextIO):
    def __init__(self, file_name, hooked_stream: TextIO):
        self.terminal = hooked_stream
        self.log = open(file_name, mode="a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


class FileLogger:
    """将 stdout 和 stderr 重定向到文件中，同时保持 stdout 和 stderr 的输出到终端，并提供一些固定的文件路径"""

    def __init__(self, output_dir, stdout_filename):
        self.output_dir = output_dir
        self.output_file = self.get_path(stdout_filename)
        os.makedirs(self.output_dir, exist_ok=False)  # Fail on exist
        os.makedirs(os.path.join(self.output_dir, "vis"), exist_ok=False)

        print(self.output_file)
        self._stdout_hooked = False
        self._stderr_hooked = False
        self.hook_stdout()
        self.hook_stderr()

    def hook_stdout(self):
        if self._stdout_hooked:
            warnings.warn("stdout already hooked")
        sys.stdout = DualOutput(self.output_file, sys.stdout)
        self._stdout_hooked = True

    def hook_stderr(self):
        if self._stderr_hooked:
            warnings.warn("stderr already hooked")
        sys.stderr = DualOutput(self.output_file, sys.stderr)
        self._stderr_hooked = True

    def write(self, msg, p=True):
        if self._stdout_hooked:
            print(msg)
            return

        with open(self.output_file, mode="a", encoding="utf-8") as log_file:
            log_file.writelines(msg + "\n")
        if p:
            print(msg)

    def get_path(self, filename):
        return os.path.join(self.output_dir, filename)

    def get_timestamped_vis_path(self, suffix):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join("vis", timestamp + suffix)
        return self.get_path(filename)
