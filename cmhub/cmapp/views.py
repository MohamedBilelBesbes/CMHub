from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, EditProfileForm, d
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post
import pickle
from googletrans import Translator
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import xgboost as xgb
from sklearn.decomposition import PCA
import joblib

#Users
def index(request):
    return render(request, 'cmapp/index.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account was created successfully, you just need to login')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'cmapp/register.html', {'form': form})


@login_required()
def profile(request):
    posts = Post.objects.filter(owner=request.user.username)
    args = {'posts':posts}
    return render(request, 'cmapp/profile.html', args)
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
        return redirect('display_posts')

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
        numberoffollowers = post.numberoffollowers
        numberoffollowing = post.numberoffollowing
        numberoftweets = post.numberoftweets
        picture = post.picture
        video = post.video
        content = post.content
        if picture == False:
            picture = 0
        elif picture == True :
            picture= 1
        if video == False:
            video = 0
        elif video == True :
            video= 1
        numberOfHashtags = content.count('#')
        numberOfTags = content.count('@')
        numberOfURLs = content.count('http')
        with open('.//cmhub//cmapp//pickles//Encoder.pkl', 'rb') as pkl:
            encoder2 = pickle.load(pkl)
        encoder = joblib.load('.//cmhub//cmapp//pickles//Encoder.pkl', 'rb')
        retweet_model = xgb.Booster()
        retweet_model.load_model(".//cmhub//cmapp//pickles//retweetmodel.bin")
        like_model = xgb.Booster()
        like_model.load_model(".//cmhub//cmapp//pickles//likemodel.bin")
        comment_model = xgb.Booster()
        comment_model.load_model(".//cmhub//cmapp//pickles//commentsmodel.bin")
        with open('.//cmhub//cmapp//pickles//commentscaler.pkl', 'rb') as pkl:
            commentscaler = pickle.load(pkl)
        with open('.//cmhub//cmapp//pickles//Scaler.pkl', 'rb') as pkl:
            scaler = pickle.load(pkl)
        with open('.//cmhub//cmapp//pickles//pcapurl.pkl', 'rb') as pkl:
            pcapurl = pickle.load(pkl)
        with open('.//cmhub//cmapp//pickles//pcavtag.pkl', 'rb') as pkl:
            pcavtag = pickle.load(pkl)
        translator = Translator()
        language = 'unknown'
        try:
            language = translator.detect(post.content).lang
        except:
            pass
        language = d[language]
        #language = pd.DataFrame(data={'language' : language}, index=['language'])
        #language['language'].iloc[0]
        #language = encoder.transform(language)
        data = {'NumberofTweets':[numberoftweets for i in range(4)], 'NumberofFollowing':[numberoffollowing for i in range(4)], 'NumberofFollowers':[numberoffollowers for i in range(4)],'Picture':[picture for i in range(4)],'Video':[video for i in range(4)], 'numberOfHashtags':[numberOfHashtags for i in range(4)], 'numberOfTags':[numberOfTags for i in range(4)], 'numberOfURLs':[numberOfURLs for i in range(4)],'tweetage':[i for i in range(1,5)],'language':[language for i in range(4)]}
        df = pd.DataFrame(data)
        df1= df.copy()
        print('---------------')
        print(df.head(5))
        print('---------------')
        df[['NumberofTweets', 'NumberofFollowing', 'NumberofFollowers', 'numberOfHashtags', 'numberOfTags', 'numberOfURLs','tweetage','language']] = scaler.transform(df[['NumberofTweets', 'NumberofFollowing', 'NumberofFollowers', 'numberOfHashtags', 'numberOfTags', 'numberOfURLs','tweetage','language']])
        picurls = df[['Picture' , 'numberOfURLs']]
        videotags = df[['Video' , 'numberOfTags']]
        videotags = pcavtag.transform(videotags)
        picurls = pcapurl.transform(picurls)
        df['VideoNTags'] = videotags.reshape(1,-1)[0]
        df['PictureNURL'] = picurls.reshape(1,-1)[0]
        df = df.drop(columns=['Video' , 'numberOfTags' , 'Picture' , 'numberOfURLs'])
        y_pretweet = pd.Series(retweet_model.predict(xgb.DMatrix(df.values))).apply(lambda x : 10**x) - 1
        y_pretweet = y_pretweet.round().astype('int64')
        y_retweet = sorted(y_pretweet.tolist())
        y_retweet = [max(0,y_retweet[i]) for i in range(len(y_retweet))]
        y_prlike = pd.Series(like_model.predict(xgb.DMatrix(df.values))).apply(lambda x : 10**x) - 1
        y_prlike = y_prlike.round().astype('int64')
        y_like = sorted(y_prlike.tolist())
        y_like = [max(0,y_like[i]) for i in range(len(y_like))]
        df1 =df1[['NumberofTweets', 'NumberofFollowing', 'NumberofFollowers', 'tweetage', 'numberOfHashtags']]
        print(df1.head(3))
        df1[['NumberofTweets', 'NumberofFollowing', 'NumberofFollowers', 'numberOfHashtags',  'tweetage']] = commentscaler.transform(df1[['NumberofTweets', 'NumberofFollowing', 'NumberofFollowers', 'numberOfHashtags',  'tweetage']])
        y_prcomments = pd.Series(comment_model.predict(xgb.DMatrix(df1.values))).apply(lambda x : x / 10)
        y_prcomments =  y_prcomments.round().astype('int64')
        y_prcomments = sorted( y_prcomments.tolist())
        y_prcomments = [max(0,y_prcomments[i]) for i in range(len(y_prcomments))]
        args = {'post':post,'y_retweet':y_retweet, 'y_like':y_like, 'y_comment':y_prcomments}
        return render(request, 'posts/display_post.html', args)
