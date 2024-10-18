import gradio as gr
import time
import tempfile
import os


css = """
#warning {background-color: #FFCCCB}
.feedback textarea {font-size: 24px !important}
.mygray {
  color: var(--gray-100);
}
.disabled-button {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #cccccc;
  color: #666666;
  border: 1px solid #999999;
}
"""


def process_video(video,request: gr.Request):
    # This is a placeholder function
    # In a real scenario, you would implement your video processing logic here
    processed_video = video
    print(video)
    print("session_hash", request.session_hash)
    
    print("Process finished.")
    btn = gr.DownloadButton(label="Download Video", value=processed_video, visible=True, elem_id=None, elem_classes=None)
    return video, btn


def clear_click():
    return None, None, gr.DownloadButton(label="Download Video", visible=True, value=None, elem_classes="disabled-button")

with gr.Blocks(css=css) as demo:
    with gr.Row():
        with gr.Column(scale=1):
            input_video = gr.Video(label="Upload Video")
            with gr.Row():
                clear_btn = gr.Button("Clear")
                process_btn = gr.Button("Process")
        with gr.Column(scale=1):
            output_video = gr.Video(label="Processed Video", show_download_button=False)
            download_btn = gr.DownloadButton(label="Download Video", visible=True,  elem_classes="disabled-button")

    process_btn.click(
        fn=process_video,
        inputs=input_video,
        outputs=[output_video, download_btn]
    )

    clear_btn.click(
        fn=clear_click,
        inputs=None,
        outputs=[input_video,output_video, download_btn],
    )

   
demo.launch(server_port=9990, allowed_paths=["./file"])


