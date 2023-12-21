from downloader.parser.args import init_parser
from downloader.annotations import generate_from_playlist, generate_from_video
from downloader.utils.json_crud import create_json, read_json
from downloader.utils.utils import (
    compare_and_merge_lists,
    compare_list_to_folder,
    make_directory,
)
from downloader.downloader.downloader import Downloader
from downloader.logger.logger import logger
from pytube import Playlist, YouTube
import os
from downloader.constants import (
    WELCOME,
    END,
    ALL_DOWNLOADED,
    NOT_JSON_FILE,
    NO_URL_PROVIDED,
    JSON_FOUND_MERGING,
    NO_URL_PROVIDED,
    NO_DOWNLOAD_FLAG,
)


if __name__ == "__main__":
    args = init_parser()
    logger.info(WELCOME)
    if args.url:
        logger.info(f"URL provided: {args.url}")
        if args.type == "playlist":
            playlist = generate_from_playlist(Playlist(args.url))
        else:
            playlist = generate_from_video(YouTube(args.url))

        if os.path.isfile(args.file_json):
            logger.info(JSON_FOUND_MERGING)
            merged_playlist = compare_and_merge_lists(
                read_json(args.file_json), playlist
            )
            create_json(args.file_json, merged_playlist)
        else:
            create_json(args.file_json, playlist)
    else:
        logger.info(NO_URL_PROVIDED)
        if os.path.isfile(args.file_json):
            playlist = read_json(args.file_json)
            playlist = compare_and_merge_lists(read_json(args.file_json), playlist)
            create_json(args.file_json, playlist)
        else:
            logger.info(NOT_JSON_FILE)

    if args.download:
        missing_videos = compare_list_to_folder(
            read_json(args.file_json), args.output_path
        )
        if len(missing_videos) != 0:
            logger.info(f"Downloading {len(missing_videos)} videos")
            make_directory(args.output_path)
            for video in missing_videos:
                Downloader(video["url"], args.output_path).download_yt()
        else:
            logger.info(ALL_DOWNLOADED)
    else:
        logger.info(NO_DOWNLOAD_FLAG)

    logger.info(END)
