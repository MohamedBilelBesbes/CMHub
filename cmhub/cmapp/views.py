from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post

#Users
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
@login_required()
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
@login_required()
def delete_user(request,pk):
    user = User.objects.filter(username=pk)
    user.delete()
    return redirect('index')

#Posts
def create_post(request, owner):
    # ...
    if request.method == 'POST':
       
        Numberoffollowers = int(request.POST.get('numberoffollowers'))
        Numberoffollowing = int(request.POST.get('numberoffollowing'))
        Numberoftweets = int(request.POST.get('numberoftweets'))
      
        Content = str(request.POST.get('content'))
        Picture = request.POST.get('picture')
        video = request.POST.get('video')
        
        Owner=User.objects.get(pk=owner).username
        if video == "no":
            video=False
        elif video == "yes" :
            video=True
        
        if Picture == "no":
            Picture=False
        elif Picture == "yes" :
            Picture=True
        post = Post.objects.create(
              numberoffollowers = Numberoffollowers,
              numberoffollowing = Numberoffollowing,
              numberoftweets = Numberoftweets,
              content = Content,
              picture = Picture,
              video = video,
              owner = Owner,

            )
        return redirect('index')

    return render(request, 'posts/createposts.html')
@login_required()
def display_posts(request):
        posts = Post.objects.all()
        args = {'posts': posts}
        return render(request, 'posts/display_posts.html', args)
@login_required()
def delete_post(request,pk):
    post = Post.objects.filter(pk=pk)
    post.delete()
    return redirect('index')
@login_required()
def edit_post(request,idpost):
    if request.method == 'POST':
        post = Post.objects.filter(pk=idpost)
        Numberoffollowers = int(request.POST.get('numberoffollowers'))
        Numberoffollowing = int(request.POST.get('numberoffollowing'))
        Numberoftweets = int(request.POST.get('numberoftweets'))
      
        Content = str(request.POST.get('content'))
        Picture = request.POST.get('picture')
        video = request.POST.get('video')
        
        #Owner=User.objects.get(pk=owner).username
        if video == "no":
            video=False
        elif video == "yes" :
            video=True
        
        if Picture == "no":
            Picture=False
        elif Picture == "yes" :
            Picture=True
        post.update(
              numberoffollowers = Numberoffollowers,
              numberoffollowing = Numberoffollowing,
              numberoftweets = Numberoftweets,
              content = Content,
              picture = Picture,
              video = video,
              

            )
        return redirect('index')
    else :
        post = Post.objects.get(pk=idpost)
        Picture = post.picture
        Video = post.video
        if Picture == False:
            Picture = "no"
        elif Picture == True :
            Picture= "yes"
        if Video == False:
            Video = "no"
        elif Video == True :
            Video= "yes"
        args = {'post' : post, 'picture': Picture, 'video': Video}
        

    return render(request, 'posts/edit_post.html', args)
@login_required()
def display_post(request, pk):
        post = Post.objects.get(pk=pk)
        args = {'post': post}
        return render(request, 'posts/display_post.html', args)