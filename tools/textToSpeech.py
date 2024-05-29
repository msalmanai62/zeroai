from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import os
# import soundfile as sf

models_path = "C:\\Users\\PMYLS\\Documents\\Projects\\Zero-Ai\\backend\\tools\\trained_models"

def text_to_Speech(text):
    processor = SpeechT5Processor.from_pretrained(os.path.join(models_path, "speecht5_tts"))
    model = SpeechT5ForTextToSpeech.from_pretrained(os.path.join(models_path, "speecht5_tts"))
    vocoder = SpeechT5HifiGan.from_pretrained(os.path.join(models_path, "speecht5_hifigan"))
    inputs = processor(text=text, return_tensors="pt")
    # load xvector containing speaker's voice characteristics from a dataset
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    return speech