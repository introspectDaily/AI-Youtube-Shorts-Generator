import gradio as gr
import os
import tempfile
import shutil
from Components.FaceCrop import crop_to_vertical, combine_videos
from Components.Speaker import detect_faces_and_speakers
from Components.LanguageTasks import GetHighlight
from Components.Transcription import transcribe_video  # Assuming this function exists
import logging
import subprocess
import uuid
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_session_id():
    return str(uuid.uuid4())

def ensure_session_directory(session_id):
    session_dir = os.path.join("seesions", session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def convert_to_mp4(input_path, output_path):
    try:
        command = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-y',
            output_path
        ]
        subprocess.run(command, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting video: {e.stderr.decode()}")
        raise

def create_highlight_video(input_video, start_time, end_time, output_path):
    with VideoFileClip(input_video) as video:
        highlight = video.subclip(start_time, end_time)
        highlight.write_videofile(output_path)

def process_video(video_path, session_id, progress=gr.Progress()):
    try:
        session_dir = ensure_session_directory(session_id)
        
        # Generate output file paths
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        cropped_path = os.path.join(session_dir, f"{base_name}_cropped.mp4")
        final_path = os.path.join(session_dir, f"{base_name}_final.mp4")
        highlight_path = os.path.join(session_dir, f"{base_name}_highlight.mp4")
        
        # Process the video
        progress(0.1, desc="Detecting faces and speakers")
        detect_faces_and_speakers(video_path, os.path.join(session_dir, "DecOut.mp4"))
        
        progress(0.3, desc="Cropping video to vertical format")
        crop_to_vertical(video_path, cropped_path)
        
        progress(0.5, desc="Combining audio with cropped video")
        combine_videos(video_path, cropped_path, final_path)
        
        progress(0.6, desc="Transcribing video")
        transcription = transcribe_video(final_path)  # Assuming this function exists
        
        progress(0.7, desc="Generating highlight")
        start_time, end_time = GetHighlight(transcription)
        
        progress(0.9, desc="Creating highlight video")
        create_highlight_video(final_path, start_time, end_time, highlight_path)
        
        progress(1.0, desc="Processing complete")
        
        return highlight_path
    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        # Return the original video if processing fails
        return video_path

def gradio_interface(input_video):
    if input_video is None:
        raise gr.Error("Please upload a video file.")
    
    # Generate a new session ID for each video processing request
    session_id = generate_session_id()
    
    # Process the video
    try:
        output_video = process_video(input_video, session_id)
        if not os.path.exists(output_video):
            raise gr.Error("Processed video file not found.")
        return output_video
    except Exception as e:
        logging.error(f"Video processing failed: {str(e)}")
        return input_video  # Return the original video if processing fails

# Create Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Video(label="Upload Video"),
    outputs=gr.Video(label="Highlighted Video"),
    title="AI YouTube Shorts Generator",
    description="Upload a video to process and create a highlight suitable for YouTube Shorts.",
    allow_flagging="never"
)

# Launch the interface
if __name__ == "__main__":
    iface.launch(allowed_paths=["./seesions"])
