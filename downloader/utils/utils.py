from downloader.logger.logger import logger
import os


def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"{directory} created")
    else:
        logger.info(f"{directory} folder already exists")


def compare_and_merge_lists(old, new):
    # Confronta le liste
    if old != new:
        return old + new
    else:
        return new


def compare_list_to_folder(list, folder):
    videos_in_folder = os.listdir(folder)

    return [
        item["title"] for item in list if f"{item['title']}.mp4" not in videos_in_folder
    ]


def compare_list_to_folder(list, folder):
    files_in_folder = [
        f[:-4] for f in os.listdir(folder) if f.endswith(".mp4")
    ]  # rimuove l'estensione .mp4

    return [item for item in list if item["title"] not in files_in_folder]


def std_str(string: str):
    return string.replace(" ", "_").replace("-", "_")
