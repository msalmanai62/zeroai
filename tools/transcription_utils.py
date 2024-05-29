import os
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import librosa
from moviepy.editor import VideoFileClip
# C:\Users\PMYLS\Documents\Projects\Zero-Ai\backend\tools\trained_models\wav2vec2-base-960h
model_name1="C:\\Users\\PMYLS\\Documents\\Projects\\Zero-Ai\\backend\\tools\\trained_models\\wav2vec2-base-960h"

def load_and_resample(audio_path, target_sr=16000):
    speech, original_sr = librosa.load(audio_path, sr=None)
    if original_sr != target_sr:
        speech = librosa.resample(speech, orig_sr=original_sr, target_sr=target_sr)
    return speech, target_sr

def extract_audio_from_video(video_path, audio_output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output_path)
    return audio_output_path

def transcribe_audio(audio_path, model_name=model_name1):
    tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    speech, _ = load_and_resample(audio_path, target_sr=16000)
    input_values = tokenizer(speech, return_tensors="pt", padding="longest").input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])
    return transcription

def transcribe_file(file_path):
    audio_extensions = ['.wav', '.mp3', '.flac', '.aac']
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext in audio_extensions:
        return transcribe_audio(file_path)
    elif file_ext in video_extensions:
        audio_file = "temp_audio.wav"
        extract_audio_from_video(file_path, audio_file)
        transcription = transcribe_audio(audio_file)
        os.remove(audio_file)
        return transcription
    else:
        raise ValueError("Unsupported file format")
