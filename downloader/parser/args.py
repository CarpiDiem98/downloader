import argparse


def init_parser():
    parser = argparse.ArgumentParser(description="Downloader for yt videos")
    parser.add_argument(
        "--url",
        type=str,
        help="url of the video or playlist",
    )
    parser.add_argument(
        "--generate_json",
        type=bool,
        default=True,
        help="generate the json file",
    )
    parser.add_argument(
        "--download",
        type=bool,
        default=False,
        help="download the videos",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="output",
        help="output path",
    )
    parser.add_argument(
        "--file_json",
        type=str,
        default="annotations.json",
        required=False,
        help="path to the json file",
    )

    return parser.parse_args()
