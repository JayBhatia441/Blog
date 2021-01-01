from django import forms
from blog.models import Blog,Comment,Category,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

choices = User.objects.all()

class UserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields = ('username','first_name','last_name')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('category','title','text','header_image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),

            'text': forms.Textarea(attrs={'class': 'textinputclass'}),

        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
