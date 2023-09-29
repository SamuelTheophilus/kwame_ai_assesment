import logging
import os

def logging_setup(logging_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)
    formatter = logging.Formatter("%(levelname)s::%(asctime)s::%(name)s::%(message)s")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_path = os.path.join(project_root, "logs", "logs.log")

    handler = logging.FileHandler(log_path)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
