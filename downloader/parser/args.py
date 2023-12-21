import argparse


def init_parser():
    parser = argparse.ArgumentParser(description="Downloader for yt videos")
    parser.add_argument(
        "--url",
        type=str,
        help="url of the video or playlist",
    )
    parser.add_argument(
        "--file_json",
        type=str,
        default="annotations.json",
        help="path to the json file",
    )

    return parser.parse_args()
