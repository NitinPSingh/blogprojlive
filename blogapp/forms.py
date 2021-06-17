from django import forms
from django.contrib.auth.models import User
from .models import Post,Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','head_image','body')

        widgets={
        'head_image' : forms.FileInput(attrs={'class':'form-control'}),
        'title' : forms.TextInput(attrs={'class':'form-control'}),


        'body':forms.Textarea(attrs={'class':'form-control'}),

        }
class EditForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','body')

        widgets={
        'title' : forms.TextInput(attrs={'class':'form-control'}),


        'body':forms.Textarea(attrs={'class':'form-control'})
        }
class CommentForm(forms.ModelForm):
    text = forms.Textarea()
    
    class Meta():
        model = Comment
        fields = ( 'text',)
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True, max_length=30,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'name': 'username'}))
    password = forms.CharField(label="Password", required=True, max_length=30,
                           widget=forms.PasswordInput(attrs={
                               'class': 'form-control',
                               'name': 'password'}))
