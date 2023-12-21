from pytube import Playlist, YouTube
from downloader.logger.logger import logger
from downloader.utils.utils import std_str


def generate_from_playlist(playlist: Playlist):
    annotations = []
    for url in playlist:
        youtube = YouTube(url)
        annotations.append(
            {
                "title": std_str(youtube.title),
                "url": url,
            }
        )
    logger.info(f"Generate {len(annotations)} videos")
    return annotations


def generate_from_video(video: YouTube):
    annotations = []
    annotations.append(
        {
            "title": std_str(video.title),
            "url": video.watch_url,
        }
    )
    logger.info(f"Generate videos")
    return annotations


def check_url(url):
    try:
        return Playlist(url)
    except KeyError:
        return YouTube(url)
