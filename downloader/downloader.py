from pytube import Playlist
from downloader.logger.logger import logger


def generate_playlist(playlist_url):
    annotations = []
    playlist = Playlist(playlist_url)

    for i, url in enumerate(playlist):
        annotations.append(
            {
                # "id": i,
                "url": url,
            }
        )
        # video = url.streams.first().download()
    logger.info(f"Find {len(annotations)} videos")
    return annotations
