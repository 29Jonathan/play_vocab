from django import forms
from .models import Vocab
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VocabForm(forms.ModelForm):
    class Meta:
        model = Vocab
        fields = ['word', 'category', 'status', 'meaning', 'example']  # Include fields you want in the form
        

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user