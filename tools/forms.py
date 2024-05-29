from django import forms
from .models import UploadedFile, TextToSpeech

################ audio, vidoe upload form #################
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        labels = {
            'file': 'Select Audio or Video File'
        }
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'accept': 'audio/*,video/*'
            })
        }
        help_texts = {
            'file': 'Max size: 50 MB'
        }

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 10485760:  # 10 MB limit
                raise forms.ValidationError("File size must be under 10 MB")
            return file
        else:
            raise forms.ValidationError("Couldn't read uploaded file")

###################### text to speech form ###############

class TextToSpeechForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder': 'Enter your text here',
        'rows': 4,
        'style': 'width:100%; height:100px;'
    }))
    class Meta:
        model=TextToSpeech
        fields = ['text']