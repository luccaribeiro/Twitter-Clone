from django import forms

from main.models import Profile, Reply, Tweet, Retweet


class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100",
                "id": "formzinho",
                "rows": "3",
                "placeholder": "Tweete sua resposta",
            }
        )
    )

    class Meta:
        model = Reply
        fields = ["content"]


class PostForm(forms.ModelForm):
    content = forms.CharField(
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


class RtForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100",
                "id": "formzinho",
                "rows": "3",
                "placeholder": "Adicionar um comentário",
            }
        )
    )

    class Meta:
        model = Retweet
        fields = ["content"]

    # ----- como colocar o botão tuitar dentro da caixa de tuite -----


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={"class": "LAURA", "id": "nickname"})
    )
    bio = forms.CharField(widget=forms.TextInput(attrs={"class": "LAURA", "id": "bio"}))

    class Meta:
        model = Profile
        fields = ["nickname", "avatar", "capa", "bio"]
