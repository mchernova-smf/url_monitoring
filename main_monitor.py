import requests
import argparse
import logging
import logging.config
from time import time
from datetime import datetime
import json
from http import HTTPStatus
from bs4 import BeautifulSoup as bs
from utils.database import insert
import sqlite3

logging.config.fileConfig(f'utils/logging.conf')

# create logger
logger = logging.getLogger('url monitoring')


def get_url_configs(file_path):
    with open(file_path, 'r') as f:
        url_configs = json.load(f)
    return url_configs


def validate_content(text, requirements):
    html = bs(text, "lxml")
    if html.h1.text != requirements["title"]:
        logger.error(
            f"   Content doesn't match requirements. Title '{html.h1.text}' is not '{requirements['title']}'")
        return "FAIL"
    return "SUCCESS"


def validate(config):
    update_time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    try:
        logger.info(f"Validating {config['url']}")
        # measure time
        start = time()
        response = requests.get(config["url"])
        request_time = round(time() - start, 3)
        logger.info(f"   Request time: {request_time:.2f} seconds")
        # status code
        status_code = response.status_code
        status_name = HTTPStatus(status_code).name
        logger.info(f"   Response code: {status_code}, {status_name}")
        # validate content
        if response.ok:
            logger.info("   Validate content")
            content_validation = validate_content(response.text, config["content_requirements"])
        else:
            logger.info(f"   Site is down")
        logger.info(f"   Insert record to database")
        insert(config['url'], update_time, request_time, status_code, status_name, content_validation)
    except requests.exceptions.MissingSchema as e:
        logger.error(f"   Invalid url schema: {config['url']}")
        insert(config['url'], update_time, -1, -1, "Invalid url schema", "N/A")
    except requests.exceptions.ConnectionError:
        logger.error(f"   Failed to establish a new connection")
        insert(config['url'], update_time, -1, -1, "Failed to establish a new connection", "N/A")
    except sqlite3.OperationalError:
        logger.error(f"   Failed to store to database")


def main(args):
    try:
        logger.info(f"Reading configuration file: {args.urls_file_path}")
        url_configs = get_url_configs(args.urls_file_path)
        for config in url_configs:
            validate(config)
    except FileNotFoundError:
        logger.error(f"File not found {args.urls_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--urls_file_path', help='path to urls file')
    args = parser.parse_args()
    logger.info(f"Input arguments: {args}")
    main(args)
