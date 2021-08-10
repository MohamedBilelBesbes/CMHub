from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {forms.PasswordInput(attrs={'class': 'form-control', 'style':'background-color: #d0d4f5 !important;width: 40%;','placeholder':'Confirm Password ...'}),
        }


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


d = {'am': 0,
 'ar': 1,
 'bn': 2,
 'ca': 3,
 'co': 4,
 'cs': 5,
 'da': 6,
 'de': 7,
 'el': 8,
 'en': 9,
 'es': 10,
 'fa': 11,
 'fr': 12,
 'ga': 13,
 'gd': 14,
 'gl': 15,
 'gu': 16,
 'ha': 17,
 'hi': 18,
 'hu': 19,
 'id': 20,
 'it': 21,
 'iw': 22,
 'ja': 23,
 'kn': 24,
 'ko': 25,
 'lt': 26,
 'lv': 27,
 'mn': 28,
 'mr': 29,
 'ms': 30,
 'my': 31,
 'ne': 32,
 'nl': 33,
 'no': 34,
 'pl': 35,
 'pt': 36,
 'ru': 37,
 'rw': 38,
 'sd': 39,
 'sk': 40,
 'so': 41,
 'su': 42,
 'sv': 43,
 'sw': 44,
 'ta': 45,
 'te': 46,
 'th': 47,
 'tl': 48,
 'tr': 49,
 'unknown': 50,
 'ur': 51,
 'vi': 52,
 'xh': 53,
 'zh-CN': 54}