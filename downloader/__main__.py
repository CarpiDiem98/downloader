from downloader.parser.args import init_parser
from downloader.annotations import (
    check_url,
    generate_from_playlist,
    generate_from_video,
)
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

if __name__ == "__main__":
    logger.info(
        """
      ___________________
     |Starting Downloader|
     |v0.0.1             |
     |by: Carpi          |
     |___________________|
    """
    )
    args = init_parser()
    if args.url:
        if check_url(args.url) is Playlist:
            playlist = generate_from_playlist(Playlist(args.url))
        else:  # is YouTube
            playlist = generate_from_video(YouTube(args.url))

        # merge all the videos in one list
        if os.path.isfile(args.file_json):
            logger.info(f"{args.file_json} already exists")
            merged_playlist = compare_and_merge_lists(
                read_json(args.file_json), playlist
            )
            create_json(args.file_json, merged_playlist)
        else:
            create_json(args.file_json, playlist)
    else:
        logger.info("No URL provided, check file json")
        if os.path.isfile(args.file_json):
            logger.info(f"{args.file_json} already exists")
            playlist = read_json(args.file_json)
            playlist = compare_and_merge_lists(read_json(args.file_json), playlist)
            create_json(args.file_json, playlist)
        else:
            logger.info("No json file found, please provide an url or check --help")

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
            logger.info("All videos are already downloaded")
