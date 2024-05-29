from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from accounts.models import Hist
from django.utils.translation import gettext, gettext_lazy as _


class EditUserForm(UserCreationForm):
    password2 = forms.CharField(label='Password(again)', widget=forms.PasswordInput(attrs={'class':'form-control forms_class_custom'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control forms_class_custom'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username':forms.TextInput(attrs={'class':"form-control forms_class_custom"}),
            'first_name':forms.TextInput(attrs={'class':"form-control forms_class_custom"}),
            'last_name':forms.TextInput(attrs={'class':"form-control forms_class_custom"}),
            'email':forms.EmailInput(attrs={'class':"form-control forms_class_custom"}),
        }

class EditAdminProfile(UserChangeForm):
    class Meta:
        model = User
        fields='__all__'

class EditUserProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']
        widgets = {
            'username':forms.TextInput(attrs={'class':"form-control"}),
            'first_name':forms.TextInput(attrs={'class':"form-control"}),
            'last_name':forms.TextInput(attrs={'class':"form-control"}),
            'email':forms.EmailInput(attrs={'class':"form-control"}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control forms_class_custom'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control forms_class_custom'}))


class PromptForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder': 'Enter your text here',
        'rows': 5,
        'style': 'width:100%; height:150px;'
    }), label='')
    class Meta:
        model = Hist
        fields = ['text']
        # help_texts = {
        #     'text':'Enter your text here'
        # }

        # widgets = {
        #     'text':forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Enter your prompt here'}),
        #     # 'ai':forms.TextInput(attrs={'class':"form-control"}),
        #     # 'hu':forms.Textarea(attrs={'class':"form-control"}),
        # }
        # def __init__(self, *args, **kwargs):
        #     super(PromptForm, self).__init__(*args, **kwargs)
        #     # Example of setting the size using CSS
        #     self.fields['text'].widget.attrs.update({'style': 'width:100%; height:150px;'})


# class UpdatePostForm(forms.ModelForm):
#     class Meta:
#         model = Hist
#         fields = ['title', 'desc']

#         widgets = {
#             'title':forms.TextInput(attrs={'class':"form-control"}),
#             # 'author':forms.TextInput(attrs={'class':"form-control"}),
#             'desc':forms.Textarea(attrs={'class':"form-control"}),
#         }