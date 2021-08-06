from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'cmapp/edit_profile.html', args)

def delete_user(request,pk):
    user = User.objects.filter(username=pk)
    user.delete()
    return redirect('index')

