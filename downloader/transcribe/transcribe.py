import whisper
from downloader.logger.logger import logger
import os


def transcribe(model_dimension, audio_path, output):
    model = whisper.load_model(model_dimension)
    transcript_dict = whisper.transcribe(model, audio_path, verbose=False)

    logger.info("Generate file transcript")

    with open(
        os.path.join(output, os.path.basename(audio_path).split(".")[0]) + ".txt", "w"
    ) as f:
        for segment in transcript_dict["segments"]:
            f.write(
                f"{round(segment['start'], 3)} -- {round(segment['end'], 3)} -- {segment['text']}\n"
            )
