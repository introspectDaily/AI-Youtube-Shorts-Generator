# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base", torch_dtype=torch.float16)


pipe.save_pretrained("/worspace/whisper-base")