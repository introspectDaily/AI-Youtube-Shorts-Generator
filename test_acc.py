from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video, legal_path
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.FaceCrop import crop_to_vertical, combine_videos

def process_video(url, sessionid=None):
    url = url.replace(".webm", ".mp4")
    print(f"Downloaded video and audio files successfully! at {url}")
    Audio = extractAudio(url, sessionid)
    if Audio:
        transcriptions = transcribeAudio(Audio) # 调用whispermodel, audio to text
        if len(transcriptions) > 0:
            TransText = ""
            for text, start, end in transcriptions:
                TransText += (f"{start} - {end}: {text}")

            start , stop = GetHighlight(TransText)  # 调用gpt-4o, 获取高亮文本区间
            if start != 0 and stop != 0:
                print(f"Start: {start} , End: {stop}")
                output_video_path = legal_path("Out.mp4", sessionid)
                crop_video(url, output_video_path, start, stop) # 剪裁视频

                croped_video_path = legal_path("croped.mp4", sessionid)
                crop_to_vertical(output_video_path, croped_video_path) # 生成竖屏

                final_video_path = legal_path("Final.mp4", sessionid)
                combine_videos(output_video_path, croped_video_path, final_video_path)
                return final_video_path
            else:
                print("Error in getting highlight")
        else:
            print("No transcriptions found")
    else:
        print("No audio file found")
    return ""


def process_video_without_vertical(url, sessionid=None):
    url = url.replace(".webm", ".mp4")
    print(f"Downloaded video and audio files successfully! at {url}")
    Audio = extractAudio(url, sessionid)
    if Audio:
        transcriptions = transcribeAudio(Audio) # 调用whispermodel, audio to text
        if len(transcriptions) > 0:
            TransText = ""
            for text, start, end in transcriptions:
                TransText += (f"{start} - {end}: {text}")

            start , stop = GetHighlight(TransText)  # 调用gpt-4o, 获取高亮文本区间
            if start != 0 and stop != 0:
                print(f"Start: {start} , End: {stop}")
                output_video_path = legal_path("Out.mp4", sessionid)
                crop_video(url, output_video_path, start, stop) # 剪裁视频

                return output_video_path
            else:
                print("Error in getting highlight")
        else:
            print("No transcriptions found")
    else:
        print("No audio file found")
    return None