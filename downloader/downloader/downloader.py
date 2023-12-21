from downloader.logger.logger import logger
import yt_dlp
import ffmpeg
import os

from downloader.utils.utils import std_str


class Downloader:
    def __init__(self, url, output_path) -> None:
        self.output_path = output_path
        self.url = url

    def __download_yt_audio(self):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "verbose": True,
            "outtmpl": self.output_path + "%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
        }

        if self.url is list:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url)
                ydl.download([self.url])

        self.aud = os.path.join(self.output_path, std_str(info_dict["title"]))

    def __download_yt_video(self):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "verbose": True,
            "outtmpl": self.output_path + "%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }
        if self.url is list:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url)
                ydl.download([self.url])

        self.vid = os.path.join(self.output_path, std_str(info_dict["title"]))

    def __combine_audio_video(self):
        try:
            logger.info("Combine audio and video")
            input_video = ffmpeg.input(self.vid)
            input_audio = ffmpeg.input(self.aud)

            output = ffmpeg.output(
                input_video.video,
                input_audio.audio,
                self.output_path,
                vcodec="copy",
                acodec="libmp3lame",
            )
            output.run()
            output.close()

            logger.info("Remove audio and video files")
            os.remove(self.aud)
            os.remove(self.vid)

        except ffmpeg.Error as e:
            logger.error(e)

    def download_yt(self):
        self.__download_yt_audio()
        self.__download_yt_video()
        self.__combine_audio_video()
        logger.info('Done!')
