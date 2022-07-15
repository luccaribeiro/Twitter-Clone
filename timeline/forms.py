from django import forms
from main.models import Tweet

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
'id':'formzinho', 'rows':'3', 'placeholder':"O que está acontecendo?" }))

    class Meta:
        model = Tweet
        fields = ['content']
