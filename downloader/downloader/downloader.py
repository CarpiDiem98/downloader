from downloader.logger.logger import logger
import yt_dlp
import ffmpeg
import os

from downloader.utils.utils import std_str


def download_audio(url, output_path):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": output_path + "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
        ],
    }

    if isinstance(url, list):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    else:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url)
            ydl.download([url])


def download_video(url, output_path):
    ydl_opts = {
        "format": "bestvideo",
        "outtmpl": output_path + "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }
    if isinstance(url, list):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    else:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url)
            ydl.download([url])

    vid = os.path.join(output_path, std_str(info_dict["title"]))
    return vid


def rename_files(output_path):
    files = os.listdir(output_path)
    for file in files:
        old_file_path = os.path.join(output_path, file)
        new_file_path = os.path.join(output_path, std_str(file))
        os.rename(old_file_path, new_file_path)


def download_yt(url, output_path):
    download_audio(url, output_path)
    rename_files(output_path)


def combine_aud_vid(aud, vid, output_path):
    try:
        input_video = ffmpeg.input(vid)
        input_audio = ffmpeg.input(aud)

        output = ffmpeg.output(
            input_video.video,
            input_audio.audio,
            output_path,
            vcodec="copy",
            acodec="libmp3lame",
        )
        output.run()
        output.close()

        os.remove(aud)
        os.remove(vid)

    except ffmpeg.Error as e:
        logger.error(e)
