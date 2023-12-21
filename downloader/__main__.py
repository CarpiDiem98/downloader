from downloader.parser.args import init_parser
from downloader.downloader import generate_playlist, download_yt
from downloader.utils.utils import read_json, append_json, create_json, make_directory
from downloader.logger.logger import logger
import os

if __name__ == "__main__":
    args = init_parser()
    logger.info(f"Downloading playlist from {args.url}")
    if args.url is None:
        logger.info("No URL provided")
    else:
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

    if args.download:
        make_directory("output")
        logger.info(f"Downloading videos from {args.file_json}")
        if args.file_json is None:
            logger.info("No file provided")
        else:
            annotations = read_json(args.file_json)
            for annotation in annotations:
                download_yt(annotation["url"], output_path="output")
                break
