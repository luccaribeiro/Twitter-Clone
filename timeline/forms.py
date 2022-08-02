from django import forms

from main.models import Profile, Tweet


class PostForm(forms.ModelForm):
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100",
                "id": "formzinho",
                "rows": "3",
                "placeholder": "O que está acontecendo?",
            }
        )
    )

    class Meta:
        model = Tweet
        fields = ["content"]


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={"class": "LAURA", "id": "nickname", "placeholder": "Nickname"})
    )
    bio = forms.CharField(widget=forms.TextInput(attrs={"class": "LAURA", "id": "bio", "placeholder": "Biografia"}))

    class Meta:
        model = Profile
        fields = ["nickname", "avatar", "capa", "bio"]
