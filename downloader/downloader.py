from pytube import Playlist, YouTube
from downloader.logger.logger import logger


def generate_playlist(playlist_url):
    annotations = []
    playlist = Playlist(playlist_url)

    for url in playlist:
        annotations.append(
            {
                # "id": i,
                "url": url,
            }
        )
    logger.info(f"Find {len(annotations)} videos")
    return annotations


def download_yt(url, output_path):
    pass