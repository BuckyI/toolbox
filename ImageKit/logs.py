import logging
import os


def add_file_handler(name: str, path: str = 'logs.log', match=None):
    "为 rootLogger 添加一个 handler"

    if name in [h.name for h in logging.root.handlers]:
        return  # 已经存在了就不重复添加
    handler = logging.FileHandler(path)
    handler.set_name(name)
    handler.setLevel(logging.INFO)
    if match:
        handler.addFilter(match)
    handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
    logging.root.addHandler(handler)  # add handler to root logger
    logging.debug("add log handler '%s' to '%s', log at file: '%s'",
                  handler.name, logging.root.name, path)
