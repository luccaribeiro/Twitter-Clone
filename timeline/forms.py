from pyexpat import model
from django import forms
from main.models import Profile, Tweet

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
'id':'formzinho', 'rows':'3', 'placeholder':"O que está acontecendo?" }))

    class Meta:
        model = Tweet
        fields = ['content']

class ComentariosForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
'id':'formzinho', 'rows':'3', 'placeholder':"O que está acontecendo?"}))
# ----- como colocar o botão tuitar dentro da caixa de tuite -----
    class Meta:
        fields = ['content']

class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'LAURA', 'id':'nickname'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'class':'LAURA', 'id':'bio'}))
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'bio']