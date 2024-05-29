from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class TextToSpeech(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='generated_audio_files/')

    def __str__(self):
        return self.text
