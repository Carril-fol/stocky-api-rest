import os
import logging

configure = False

def _configure_logger():
    global configure
    if configure:
        return

    level = logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
    configure = True

def get_logger(name: str) -> logging.Logger:
    _configure_logger()
    return logging.getLogger(name)