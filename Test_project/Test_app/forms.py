from django import forms
from .models import Vocab

class VocabForm(forms.ModelForm):
    class Meta:
        model = Vocab
        fields = ['word', 'category', 'status', 'meaning', 'example']  # Include fields you want in the form