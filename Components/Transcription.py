from faster_whisper import WhisperModel
import torch

def auto_detach_device():
    # else 'mps' if torch.backends.mps.is_available() 
    return 'cuda' if torch.cuda.is_available() else 'cpu'
def transcribeAudio(audio_path):
    try:
        print("Transcribing audio...")
        Device = auto_detach_device()
        print(Device)
        model = WhisperModel("base.en", device = Device)
        print("Model loaded")
        segments, info = model.transcribe(audio=audio_path, beam_size=5, language="en", max_new_tokens=128, condition_on_previous_text=False)
        segments = list(segments)
        # print(segments)
        extracted_texts = [[segment.text, segment.start, segment.end] for segment in segments]
        return extracted_texts
    except Exception as e:
        print("Transcription Error:", e)
        return []

if __name__ == "__main__":
    audio_path = "audio.wav"
    transcriptions = transcribeAudio(audio_path)
    print("Done")
    TransText = ""

    for text, start, end in transcriptions:
        TransText += (f"{start} - {end}: {text}")
    print(TransText)