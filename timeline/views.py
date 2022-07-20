from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from GoogleNews import GoogleNews
from main.models import Comentarios, Profile, Tweet

from .forms import ComentariosForm, PostForm

googlenews = GoogleNews()
googlenews = GoogleNews(period='d')
googlenews = GoogleNews(lang='pt', region='BR')
googlenews.search('BRASIL')


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
    postagem_ref = Tweet.objects.get(id=id)
    comentarios = Comentarios.objects.filter(tweet_id=id).all()
    if request.method == 'POST':
        form = ComentariosForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            usuario = request.user
            usuario_perfil = Profile.objects.get(user=usuario.id)
            post.user = usuario_perfil
            post.tweet_id = postagem_ref.id
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    context = {'postagem_ref': postagem_ref,
               'form': form, 'comentarios': comentarios}
    return render(request, 'timeline/postagem.html', context)


def perfil(request, username):
    usuario = User.objects.get(username=username)
    usuario_perfil = Profile.objects.get(user=usuario.id)
    postagens = usuario_perfil.tweets.all()
    context = {'usuario': usuario, 'postagens': postagens,
               'usuario_perfil': usuario_perfil}
    return render(request, 'timeline/perfil.html', context)
