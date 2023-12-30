from downloader.logger.logger import logger
import os


def _make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"{directory} created")
    else:
        logger.info(f"{directory} folder already exists")


def make_download_directory(directory):
    _make_directory(directory)
    _make_directory(os.path.join(directory, "audio"))


def make_transcript_directory(directory):
    _make_directory(directory)
    _make_directory(os.path.join(directory, "transcripts"))


def compare_and_merge_lists(old, new):
    if old != new:
        return old + new
    else:
        return new


def compare_list_to_folder(list: list, folder: str):
    files_in_folder = [
        f[:-4] for f in os.listdir(folder) if f.endswith(".mp3")
    ]  # rimuove l'estensione .mp4

    return [item for item in list if item["title"] not in files_in_folder]


def std_str(string: str):
    return (
        string.replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("⧸", "_")
        .replace("｜", "")
        .replace("|", "")
    )
