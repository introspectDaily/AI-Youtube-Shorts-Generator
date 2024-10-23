# from faster_whisper import WhisperModel
import torch
from transformers import pipeline
import librosa
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_DIR="/workspace/whisper-base"
pipe = pipeline(
  "automatic-speech-recognition",
  model=MODEL_DIR,
  chunk_length_s=30,
  device=device,
  torch_dtype=torch.float16,
)



# [{'timestamp': (0.0, 5.44), 'text': ' Mr. Quilter is the apostle of the middle classes, and we are glad to welcome his gospel.'}]
# [[segment.text, segment.start, segment.end] for segment in segments]


def transcribeAudio(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    input_features = librosa.resample(audio, sr, 16000) if sr != 16000 else audio
    input_features = np.expand_dims(input_features, axis=0)
    prediction = pipe(inputs=input_features,batch_size=8, return_timestamps=True)["chunks"]
    result = [None for _ in range(len(prediction))]
    for i in range(len(prediction)):
        result[i] = [prediction[i]['text'], *prediction['timestamp']]
    return result

def auto_detach_device():
    # else 'mps' if torch.backends.mps.is_available() 
    return 'cuda' if torch.cuda.is_available() else 'cpu'

# def transcribeAudio(audio_path):
#     try:
#         print("Transcribing audio...")
#         Device = auto_detach_device()
#         print(Device)
#         model = WhisperModel("base.en", device = Device, local_files_only=True)
#         print("Model loaded")
#         segments, info = model.transcribe(audio=audio_path, beam_size=5, language="en", max_new_tokens=128, condition_on_previous_text=False)
#         segments = list(segments)
#         # print(segments)
#         extracted_texts = [[segment.text, segment.start, segment.end] for segment in segments]
#         return extracted_texts
#     except Exception as e:
#         print("Transcription Error:", e)
#         return []

def transcribeAudio(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    input_features = librosa.resample(audio, sr, 16000) if sr != 16000 else audio
    input_features = np.expand_dims(input_features, axis=0)
    prediction = pipe(inputs=input_features,batch_size=8, return_timestamps=True)["chunks"]
    result = [None for _ in range(len(prediction))]
    for i in range(len(prediction)):
        result[i] = [prediction[i]['text'], *prediction['timestamp']]
    return result

if __name__ == "__main__":
    audio_path = "seesions/e4nikait6p4/output.mp3"
    transcriptions = transcribeAudio(audio_path)
    print("Done")
    TransText = ""
    print(transcriptions)

    print("*"*10)
    for text, start, end in transcriptions:
        TransText += (f"{start} - {end}: {text}")
    print(TransText)