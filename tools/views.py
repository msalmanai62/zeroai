from django.http import HttpResponseRedirect
from django.shortcuts import render

import os 
from django.conf import settings
# Create your views here.

from transformers import BartForConditionalGeneration, BartTokenizer
model_path = "C:\\Users\\PMYLS\\Documents\\Projects\\Zero-Ai\\backend\\tools\\trained_models\\bart"
model = BartForConditionalGeneration.from_pretrained(model_path)
tokenizer = BartTokenizer.from_pretrained(model_path)

# Dictionary mapping input lengths to summary lengths
length_mapping = {
    1000: 150,
    2000: 300,
    3000: 450,
    4000: 600,
    5000: 750
}

########################### text summarization #######################

def text_summary(request):
    if request.user.is_authenticated:
        input_text = ""
        max_length = 1000
        summary = ""
        if request.method=='POST':
            input_text = request.POST.get('input_text')
            max_length = int(request.POST.get('max_length'))
            summary_length = length_mapping[max_length]

            inputs = tokenizer(input_text, max_length=max_length, return_tensors="pt", truncation=True)
            summary_ids = model.generate(inputs["input_ids"], max_length=summary_length, num_beams=4, length_penalty=2.0, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            return render(request, 'tools/summerize.html', {
        'input_text': input_text,
        'max_length': max_length,
        'summary': summary
    })
        return render(request, 'tools/summerize.html')
    else:
        return HttpResponseRedirect('/login/')
    
########################### Language Translation #######################

from googletrans import Translator

def translate_text(request):
    if request.user.is_authenticated:
        translated_text = ""
        source_text = ""
        source_lang = ""
        dest_lang = ""

        if request.method == "POST":
            source_text = request.POST.get('source_text')
            source_lang = request.POST.get('source_lang')
            dest_lang = request.POST.get('dest_lang')

            translator = Translator()
            translation = translator.translate(source_text, src=source_lang, dest=dest_lang)
            translated_text = translation.text

        context = {
            'translated_text': translated_text,
            'source_text': source_text,
            'source_lang': source_lang,
            'dest_lang': dest_lang,
        }

        return render(request=request, template_name='tools/translate.html', context=context)
    else:
        return HttpResponseRedirect('/login/')
    

########################### Audio & Video Transcribe #######################
from .forms import UploadFileForm
# from .models import UploadedFile
from .transcription_utils import transcribe_file

def transcribe_audio_video(request):
    if request.user.is_authenticated:
        transcription = None
        file_url = None
        file_type = None
    
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.save()
                file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)
                transcription = transcribe_file(file_path)
                file_url = uploaded_file.file.url
                file_type = uploaded_file.file.name.split('.')[-1]
        else:
            form = UploadFileForm()
        
        return render(request, 'tools/transcribe.html', {
            'form': form,
            'transcription': transcription,
            'file_url': file_url,
            'file_type': file_type
        })
    else:
        return HttpResponseRedirect('/login/')

########################### Text To Speech #######################

from .textToSpeech import text_to_Speech
import soundfile as sf
import os
from django.conf import settings
from pathlib import Path
from .forms import TextToSpeechForm
from django.shortcuts import render

def text_to_speech(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TextToSpeechForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                audio_filename = f"{text[:5].replace(' ', '-')}.wav"
                audio_path = Path(settings.MEDIA_ROOT) / "generated_audio_files" / audio_filename
            
                # Ensure the directory exists
                audio_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Generate the speech and save the file
                speech = text_to_Speech(text=text)
                sf.write(str(audio_path), speech.numpy(), samplerate=16000)
                
                # Construct the audio file URL
                audio_file_url = settings.MEDIA_URL + f"generated_audio_files/{audio_filename}"
                
                context = {
                    'text': text,
                    'audio_file_url': audio_file_url,
                    'form': form,
                }
                return render(request, 'tools/textToSpeech.html', context)
        else:
            form = TextToSpeechForm()
        
        context = {'text': '', 'form': form}
        return render(request, 'tools/textToSpeech.html', context)
    else:
        return HttpResponseRedirect("/login/")

def Services_page(request):
    return render(request=request, template_name='accounts/services.html')