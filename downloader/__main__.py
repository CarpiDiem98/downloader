from downloader.parser.args import init_parser
from downloader.downloader import generate_playlist
from downloader.utils.utils import read_json, append_json, create_json
from downloader.logger.logger import logger
import os

if __name__ == "__main__":
    args = init_parser()
    logger.info(f"Downloading playlist from {args.url}")
    playlist = generate_playlist(args.url)

    if os.path.isfile(args.file_json):
        logger.info(f"{args.file_json} already exists")
        old = read_json(args.file_json)

        if old != playlist:
            logger.info(f"{args.file_json} updated")
            append_json(args.file_json, playlist)

    else:
        logger.info(f"{args.file_json} does not exists")
        create_json(args.file_json, playlist)
