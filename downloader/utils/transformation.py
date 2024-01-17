from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop


def crop_left_side(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    width, height = video_clip.size
    left_width = width // 2 - 120
    cropped_clip = crop(video_clip, x1=0, y1=0, x2=left_width, y2=height)
    cropped_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    video_clip.close()