from django.urls import path
from . import views


urlpatterns = [
    path(route='summarize/', view=views.text_summary, name='summary_url'),
    path(route='translate/', view=views.translate_text, name='translate_url'),
    path(route='transcribe/', view=views.transcribe_audio_video, name='transcribe_url'),
    path(route='textToSpeech/', view=views.text_to_speech, name='textToSpeech_url'),
    path(route='services/', view=views.Services_page, name='services_url'),
]