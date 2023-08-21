import os
import logging
import wandb


def get_logger(
    name: str,
    log_dir: str,
    log_name: str = "run.log",
    log_format: str = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S'",
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


def wandb_log_histogram(
    key,
    values,
    step=None,
    commit=True,
    sync=True,
):
    wandb.log({key: values}, step=step, commit=commit, sync=sync)
