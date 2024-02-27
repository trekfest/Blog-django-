from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, UserProfile, Category


class CreationUser(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']

    def save(self, commit=True):
        user = super(CreationUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.bio = self.cleaned_data['bio']
        if commit:
            user.save()
        return user


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Article
        fields = ['article_title', 'article_text', 'category']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']