from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'cmapp/index.html')



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'cmapp/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'cmapp/profile.html')