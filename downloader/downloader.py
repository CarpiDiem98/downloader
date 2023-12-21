from pytube import Playlist
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
