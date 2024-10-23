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