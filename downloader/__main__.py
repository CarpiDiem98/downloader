from downloader.parser.args import init_parser
from downloader.annotations import generate_from_playlist, generate_from_video
from downloader.transcribe.transcribe import transcribe
from downloader.utils.json_crud import create_json, read_json
from downloader.utils.transformation import crop_left_side
from downloader.utils.utils import (
    compare_and_merge_lists,
    compare_list_to_folder_audio,
    compare_list_to_folder_video,
    make_download_directory,
    make_transcript_directory,
)
from downloader.downloader.downloader import DownloaderVideo, DownloaderAudio
from downloader.logger.logger import logger
from pytube import Playlist, YouTube
import os
from downloader.constants import (
    DOWNLOADING_VIDEOS_MESSAGE,
    WELCOME,
    END,
    ALL_AUDIO_DOWNLOADED,
    ALL_VIDEO_DOWNLOADED,
    NOT_JSON_FILE,
    NO_URL_PROVIDED,
    JSON_FOUND_MERGING,
    NO_URL_PROVIDED,
    NO_DOWNLOAD_FLAG,
    TRANSCRIPT_FLAG,
    JSON_FOUND,
    DOWNLOADING_AUDIO_MESSAGE,
    NO_OUTPUT_PATH,
    CROPPING_VIDEO,
)


if __name__ == "__main__":
    args = init_parser()
    logger.info(WELCOME)

    if args.url:
        logger.info(f"URL provided: {args.url}")
        if args.type == "playlist":
            playlist = generate_from_playlist(Playlist(args.url))
        elif args.type == "video":
            playlist = generate_from_video(YouTube(args.url))
        else:
            logger.info("No type provided")
            exit()

        if os.path.isfile(args.file_json):
            logger.info(JSON_FOUND_MERGING)
            merged_playlist = compare_and_merge_lists(
                read_json(args.file_json), playlist
            )
            create_json(args.file_json, merged_playlist)
        else:
            create_json(args.file_json, playlist)
    else:
        logger.info(NO_URL_PROVIDED)
        if os.path.isfile(args.file_json):
            logger.info(JSON_FOUND)
            # playlist = read_json(args.file_json)
        else:
            logger.info(NOT_JSON_FILE)

    if args.output_path:
        make_download_directory(args.output_path)
        missing_audios = compare_list_to_folder_audio(
            read_json(args.file_json),
            os.path.join(args.output_path, "audio/"),
        )
        missing_videos = compare_list_to_folder_video(
            read_json(args.file_json),
            os.path.join(args.output_path, "video/"),
        )
    else:
        logger.info(NO_OUTPUT_PATH)

    if args.download:
        downloader_video = DownloaderVideo(args.output_path)
        downloader_audio = DownloaderAudio(args.output_path)
        if len(missing_audios) != 0:
            logger.info(DOWNLOADING_AUDIO_MESSAGE.format(len(missing_videos)))
            downloader_audio.download_yt_audio(missing_audios)
        else:
            logger.info(ALL_AUDIO_DOWNLOADED)

        if len(missing_videos) != 0:
            logger.info(DOWNLOADING_VIDEOS_MESSAGE.format(len(missing_videos)))
            downloader_video.download_yt_video(missing_videos)
        logger.info(ALL_VIDEO_DOWNLOADED)

    elif not args.download and args.download_audio:
        downloader_audio = DownloaderAudio(args.output_path)
        if len(missing_audios) != 0:
            logger.info(DOWNLOADING_AUDIO_MESSAGE.format(len(missing_videos)))
            downloader_audio.download_yt_audio(missing_audios)
        else:
            logger.info(ALL_AUDIO_DOWNLOADED)

    elif not args.download and args.download_video:
        downloader_video = DownloaderVideo(args.output_path)
        if len(missing_videos) != 0:
            logger.info(DOWNLOADING_VIDEOS_MESSAGE.format(len(missing_videos)))
            downloader_video.download_videos(missing_videos)
        else:
            logger.info(ALL_VIDEO_DOWNLOADED)
    else:
        logger.info(NO_DOWNLOAD_FLAG)

    if args.transcribe:
        logger.info(TRANSCRIPT_FLAG)
        make_transcript_directory(args.output_path)
        for audio in os.listdir(os.path.join(args.output_path + "audio/")):
            transcribe(
                args.model_dimension,
                os.path.join(args.output_path + "audio/", audio),
                os.path.join(args.output_path + "transcripts/"),
            )

    logger.info(CROPPING_VIDEO)
    videos = os.listdir(os.path.join(args.output_path + "video/"))
    for video in videos:
        crop_left_side(
            os.path.join("/home/emanuele/downloader/output", "video/", video),
            os.path.join(
                "/home/emanuele/downloader/output/cropped_video/",
                video.replace(".mp4", "_cropped.mp4"),
            ),
        )
    logger.info(END)
