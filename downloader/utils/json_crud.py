from typing import Dict, List
from downloader.logger.logger import logger
import json


def create_json(file_json, annotations):
    logger.info(f"Create new {file_json}")
    with open(file_json, "w") as outfile:
        json.dump(annotations, outfile)
    logger.info(f"{file_json} created")


def append_json(file_json, annotations):
    data = read_json(file_json)
    data.extend(annotations)
    with open(file_json, "w") as outfile:
        json.dump(data, outfile)

    logger.info(f"{file_json} updated")


def read_json(file_json) -> List[Dict]:
    logger.info(f"Read {file_json}")
    try:
        with open(file_json, "r") as infile:
            data = json.load(infile)
    except FileNotFoundError as e:
        logger.error(e)
    return data
