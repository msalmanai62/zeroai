from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from .forms import PromptForm, EditUserForm, LoginForm, EditAdminProfile, EditUserProfile
from django.contrib.auth import authenticate, login, logout
from .models import Hist
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch.nn.functional as F

def Home(request):
    return render(request=request, template_name='accounts/home.html', context={})

model_directory = "C:/Users/PMYLS/Documents/Projects/Zero-Ai/backend/detect-ai-text-trained-model"
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModelForSequenceClassification.from_pretrained(model_directory)

def Main(request):
    lbl=None
    prob=None
    if request.user.is_authenticated:
        if request.method=='POST':
            fm = PromptForm(request.POST)
            if fm.is_valid():
                txt = fm.cleaned_data['text']
                inputs = tokenizer(txt, return_tensors="pt")
                with torch.no_grad():
                    logits = model(**inputs).logits
                probabilities = F.softmax(logits, dim=-1)
                predicted_class_id = probabilities.argmax().item()
                predicted_probability = round(probabilities[0][predicted_class_id].item()*100, 2)
                label = model.config.id2label[predicted_class_id]
                lbl = label
                prob = predicted_probability
                aa = Hist(text=txt, label=lbl, prob=prob)
                aa.save()
                messages.success(request, 'Text sent')

                # fm = PromptForm()
                # return HttpResponseRedirect('/main/')
        else:
            fm = PromptForm()
        return render(request=request, template_name='accounts/main.html', context={'form':fm, 'lbl':lbl, 'prob':prob})
    else:
        return HttpResponseRedirect('/login/')
#contact page       
def contactpage(request):
    return render(request, template_name='accounts/contact.html', context={})

#about page
def aboutpage(request):
    return render(request, template_name='accounts/about.html', context={})

# #signup page
def signuppage(request):
    if request.method=='POST':
        fm = EditUserForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            messages.success(request, 'Your Registration is Successfull')
    else:
        fm = EditUserForm()
    return render(request, template_name='accounts/signup.html', context={'form':fm})

# #login page
def loginpage(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(request=request, username=uname, password=upass)
                if user is not None:
                    login(request=request, user=user)
                    messages.success(request=request, message='LoggedIn Successfully!!')
                    return HttpResponseRedirect('/tools/services/')
        else:
            fm=LoginForm(request)
        return render(request, template_name='accounts/login.html', context={'form':fm})
    else:
        return HttpResponseRedirect('/tools/services/')
    
# #profile page
def profilepage(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            # fm = UserChangeForm(instance=request.user)
            if request.user.is_superuser:
                fm = EditAdminProfile(request.POST, instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfile(request.POST, instance=request.user)
                users=None
            if fm.is_valid():
                fm.save()
                messages.success(request=request, message='Profile Updated Successfully!!')
        else:
            if request.user.is_superuser:
                fm = EditAdminProfile(instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfile(instance=request.user)
                users=None
        return render(request=request, template_name='accounts/profile.html', context={'form':fm, 'users':users, 'name':request.user.username})
    else:
        return HttpResponseRedirect('/login/')
    
# #logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

