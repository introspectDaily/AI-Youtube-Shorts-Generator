from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
import subprocess

import os
current_path = os.getcwd()

"""
os.path.basename(file_path)
"""

# def extractAudio(video_path):
#     try:
#         video_clip = VideoFileClip(video_path)
#         audio_path = "audio.wav"
#         video_clip.audio.write_audiofile(audio_path)
#         video_clip.close()
#         print(f"Extracted audio to: {audio_path}")
#         return audio_path
#     except Exception as e:
#         print(f"An error occurred while extracting audio: {e}")
#         return None

def legal_path(ori_path, sessionid=None):
    filename = os.path.basename(ori_path)
    if not isinstance(sessionid, str): sessionid = str(sessionid)
    _dir = os.path.join(current_path, "seesions", sessionid)
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    if sessionid:
        tag_path =  os.path.join(_dir, filename)
    else:
        print("Warning: sessionid is None") 
        tag_path =  os.path.join(current_path, filename)
    return tag_path


def extractAudio(video_path, sessionid=None):
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = legal_path("audio.wav", sessionid)
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        print(f"Extracted audio to: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return None


def crop_video(input_file, output_file, start_time, end_time):
    with VideoFileClip(input_file) as video:
        cropped_video = video.subclip(start_time, end_time)
        cropped_video.write_videofile(output_file, codec='libx264')

# Example usage:
if __name__ == "__main__":
    input_file = r"Example.mp4" ## Test
    print(input_file)
    output_file = "Short.mp4"
    start_time = 31.92 
    end_time = 49.2   

    crop_video(input_file, output_file, start_time, end_time)

