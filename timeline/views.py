from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from GoogleNews import GoogleNews
from main.models import Like, Profile, Tweet
from .forms import PostForm, ProfileForm
from django.contrib.auth.models import User


googlenews = GoogleNews()
googlenews = GoogleNews(period='d')
googlenews = GoogleNews(lang='pt', region='BR')
googlenews.get_news('Brasil')


def principal(request):
    noticias = googlenews.results()
    tweets = Tweet.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            usuario = request.user
            usuario_perfil = Profile.objects.get(user=usuario.id)
            post.user = usuario_perfil
            post.save()
            return redirect('main:timeline_page')
    else:
        form = PostForm()
    context = {'tweets': tweets, 'form': form, 'noticias': noticias}
    return render(request, 'timeline/principal.html', context)


def postagem(request, id):
    noticias = googlenews.results()
    postagem_ref = Tweet.objects.get(id=id)
    reply_list = Tweet.objects.filter(reply_to=postagem_ref.id)
    likes = Like.objects.filter(tweet_id=postagem_ref.id).count()
    rts = Tweet.objects.filter(rt_id=postagem_ref.id).count()
    replies = reply_list.count()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            usuario = request.user
            usuario_perfil = Profile.objects.get(user=usuario.id)
            post.user = usuario_perfil
            post.reply_to_id = postagem_ref.id
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    context = {'postagem_ref':postagem_ref, 'form': form, 'reply_list':reply_list, 'noticias': noticias, 'likes':likes, 'rts':rts, 'replies':replies }
    return render(request, 'timeline/postagem.html', context)


def perfil(request, username):
    usuario = User.objects.get(username=username)
    usuario_perfil = Profile.objects.get(user=usuario.id)
    postagens = usuario_perfil.tweets.all()
    context = {
        'usuario': usuario,
        'postagens': postagens,
        'usuario_perfil': usuario_perfil
    }
    return render(request, 'timeline/perfil.html', context)

def edit_perfil(request, username):
    usuario = User.objects.get(username=username)
    usuario_perfil = Profile.objects.get(user=usuario.id)
    postagens = usuario_perfil.tweets.all()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            usuario_perfil.nickname = 'temp'
            usuario_perfil.nickname = post.nickname
            usuario_perfil.avatar = post.avatar
            usuario_perfil.bio = post.bio
            # post.user_id = request.user.id
            # usuario_perfil = Profile.objects.get(user=usuario.id)
            # post.user = usuario_perfil
            # post.reply_to_id = postagem_ref.id
            usuario_perfil.save()
            return redirect(reverse('perfil', args=[usuario.username]))
    else:
        form = ProfileForm()
    context = {
        'usuario': usuario,
        'postagens': postagens,
        'usuario_perfil': usuario_perfil,
        'form': form
    }
    return render(request, 'timeline/perfil_edit.html', context)
