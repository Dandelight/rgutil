import os
import logging


def get_logger(
    name: str,
    log_dir: str,
    log_name: str = "run.log",
    log_format: str = "%(asctime)s %(levelname)s %(message)s",
    level: int = logging.INFO,
):
    logger = logging.getLogger(name)
    file_path = os.path.join(log_dir, log_name)
    hdlr = logging.FileHandler(file_path)
    formatter = logging.Formatter(log_format)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger
